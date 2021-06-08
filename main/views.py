from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddPainting, AddPaintingTry
from django.views.generic import ListView, CreateView, DetailView
from .models import Paintings, Message, Comment, PaintTries, Folder
from users.models import CustomUser, Profile
from django.urls import reverse
from django.contrib import messages as django_messages
import random
from django.db.models import Count
from taggit.models import Tag
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from actions.utils import create_action
from actions.models import Action
from django.core.mail import send_mail


class IndexListView(ListView):
    model = Paintings
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:        
            logged_user = Profile.objects.get(user=self.request.user).feed_tuner.all()
            all_slugs = [i.slug for i in logged_user]

            if not all_slugs:
                painting_list = list(Paintings.objects.all())
                painting_list = random.sample(painting_list, 10)
            else:
                all_paintings = []

                for i in range(len(all_slugs)):
                    tagg = get_object_or_404(Tag, slug=all_slugs[i])
                    object_list = Paintings.objects.filter(tags__in=[tagg]).all()
                    all_paintings.extend(list(object_list))

                # Sample randomly from all the user's feeds category
                painting_list = random.sample(all_paintings, min(len(all_paintings), 10))

            context['unread_count'] = Message.objects.filter(recepient=self.request.user, read=False).count()
            context['object_list'] = painting_list
            context['notify'] = len(Action.objects.filter(user_id__in=self.request.user.following.values_list('id',
                flat=True), read=False))
        else:
            un_auth = list(Paintings.objects.all())
            un_auth = random.sample(un_auth, 10)
            context['object_list'] = un_auth

        return context


def about(request):
    context = {}
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False))
        context['unread_count'] = Message.objects.filter(recepient=request.user, 
            read=False).count()

    return render(request, 'main/about.html', context)

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(subject, email, message)


        send_mail(subject, message, email, 
            ['site_owner@gmail.com'], fail_silently=False)

        django_messages.success(request, 'Message sent successfully')
        return redirect('contact')

    context = {}
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False))
        context['unread_count'] = Message.objects.filter(recepient=request.user, 
            read=False).count()

    return render(request, 'main/contact.html', context)

@login_required
def delete_message(request, message_id):
    single_message = Message.objects.get(id=message_id)
    if single_message.recepient == request.user:
        single_message.delete()
    return redirect('view_messages')

@login_required
def show_message(request, message_id):
    get_message = Message.objects.get(id=message_id)
    if request.user == get_message.recepient:
        get_message = Message.objects.get(id=message_id)
        get_message.read = True
        get_message.save()
    else:
        raise PermissionDenied

    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'single_message': get_message,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'main/single_message.html', context)

@login_required
def send_message(request):
    receiver = request.POST.get('painter_name')
    message = request.POST.get('message')
    painter = CustomUser.objects.filter(username=receiver).first()
    Message.objects.create(sender=request.user, recepient=painter, message=message)
    django_messages.success(request, "Message sent successfully.")
    return redirect('painter_profile', painter=receiver)

@login_required
def notifications(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
        flat=True)
    notify = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
        flat=True), read=False))

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')[:10]
    else:
        actions = None

    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'actions': actions,
        'notify': notify
    }
    return render(request, 'main/notifications.html', context)

@login_required(login_url="/login/")
def view_messages(request):
    all_messages = Message.objects.filter(recepient=request.user)
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'all_messages':all_messages,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'main/messages.html', context)

def paint(request):
    return render(request, 'main/paint.html')

@login_required
def add_comment(request):
    get_painting = Paintings.objects.get(id=request.POST.get('painting_id'))
    get_comment = request.POST.get('comment')
    new_comment = Comment(painting=get_painting, body=get_comment,
        commenter=request.user)
    new_comment.save()
    create_action(request.user, 'commented on', get_painting)

    return redirect('view_paint', pk=get_painting.id,
        paint=get_painting.slug)

class PaintingDetailView(DetailView):
    model = Paintings
    template_name = 'main/view_paint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        get_painting = context.get('paintings').id
        
        queryset = Paintings.objects.get(id=get_painting)
        painting_tag = queryset.tags.values_list('id', flat=True)
        similar_paintings = Paintings.objects.filter(
            tags__in=painting_tag).exclude(id=get_painting)
        similar_paintings = similar_paintings.annotate(
            same_tags=Count('tags')).order_by(
                '-same_tags', '-date_painted'
            )

        similar_paintings = list(similar_paintings)
        painting_list = random.sample(similar_paintings, min(len(similar_paintings), 8))

        if self.request.user.is_authenticated:
            context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                flat=True), read=False))
            context['unread_count'] = Message.objects.filter(recepient=self.request.user, 
                read=False).count()
        
        context['form'] = AddPaintingTry()
        context['similar_paintings'] = painting_list

        return context


@login_required
def add_paint_try(request):
    get_redirect = request.POST.get('redir')
    redirect_to = Paintings.objects.get(id=get_redirect)
    form = AddPaintingTry(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            paint = form.save(commit=False)
            paint.painting = redirect_to
            paint.tryer = request.user
            paint.save()
    return redirect('view_paint', pk=redirect_to.id,
        paint=redirect_to.slug)

@login_required
def view_folders(request):
    all_folders = Folder.objects.filter(user=request.user)
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'all_folders': all_folders,
    }
    return render(request, 'main/view_folders.html', context)

def download_painting(request, paint_pk):
    paint_image = Paintings.objects.get(id=paint_pk)
    route_from = request.POST.get('route')
    file_path = paint_image.painting.path

    # To view image before download like artstation use this...
    # response = FileResponse(open(file_path, 'rb'))
    # return response

    # To download directly to computer
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def folder_content(request, folder):
    folder_pics = Folder.objects.get(id=folder, user=request.user)
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'folder_pics': folder_pics.saved_painting.all().order_by('foldermember'),
        'folder_name': folder_pics.name,
        'folder_id': folder_pics.id,
    }
    return render(request, 'main/folder_content.html', context)

@login_required
def delete_folder(request, folder_pk):
    folder = Folder.objects.get(id=folder_pk)
    if folder.user == request.user:
        folder.delete()
    return redirect('view_folders')

@login_required
def delete_folder_paint(request, folder_id, paint_pk):
    painting = Paintings.objects.get(id=paint_pk)
    folder = Folder.objects.get(id=folder_id, user=request.user)
    if folder.user == request.user:
        folder.saved_painting.remove(painting)

    return redirect('folder_content', folder_id)

@login_required
def save_to_folder(request, paint_pk):
    redirect_to = Paintings.objects.get(id=paint_pk)
    if request.method == 'POST':
        folder_name = request.POST.get('folder')
        folder = Folder.objects.get(name=folder_name, user=request.user)
        folder.saved_painting.add(redirect_to)

        django_messages.success(request, 'Paint saved successfully')
        return redirect('view_paint', pk=redirect_to.id,
            paint=redirect_to.slug)

    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'folders_list': Folder.objects.filter(user=request.user),
        'paint_pk': paint_pk,
    }
    return render(request, 'main/create_or_save.html', context)

@login_required
def create_folder(request):
    paint_pk = request.POST.get('paint_id')
    name = request.POST.get('name')
    if name:
        Folder.objects.create(user=request.user, name=name)
    else:
        django_messages.warning(request, 'Empty folder name is not allowed')
    return redirect('save_paint', paint_pk)

@login_required
def add_painting(request):
    form = AddPainting()
    if request.method == 'POST':
        form = AddPainting(request.POST, request.FILES)
        if form.is_valid():
            new_paint = form.save(commit=False)
            new_paint.adder =  request.user
            new_paint.save()
            create_action(request.user, 'added', new_paint)
            return redirect(new_paint.get_absolute_url())

    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'form': form,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
    }
    return render(request, 'main/add_paint.html', context)

def mark_as_read(request):
    # a = Action.objects.exclude(user=request.user).filter(read=False)
    # for i in a:
    #     i.read = True
    #     i.save()
    return redirect('notifications')

