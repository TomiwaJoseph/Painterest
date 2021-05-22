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
from django.http import HttpResponse



def current_user(request):
    user = request.user
    return user

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
        else:
            un_auth = list(Paintings.objects.all())
            un_auth = random.sample(un_auth, 10)
            context['object_list'] = un_auth

        return context


def about(request):
    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
    }
    return render(request, 'main/about.html', context)

def contact(request):
    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
    }
    return render(request, 'main/contact.html', context)

def delete_message(request, message_id):
    single_message = Message.objects.get(id=message_id)
    single_message.delete()
    return redirect('view_messages')

def show_message(request, message_id):
    single_message = Message.objects.get(id=message_id)
    single_message.read = True
    single_message.save()

    context = {
        'single_message': single_message,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'main/single_message.html', context)

def send_message(request):
    receiver = request.POST.get('painter_name')
    message = request.POST.get('message')
    painter = CustomUser.objects.filter(username=receiver).first()
    Message.objects.create(sender=request.user, recepient=painter, message=message)
    django_messages.success(request, "Message sent successfully.")
    return redirect('painter_profile', painter=receiver)

def notifications(request):
    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'main/notifications.html', context)

def view_messages(request):
    all_messages = Message.objects.filter(recepient=request.user)
    context = {
        'all_messages':all_messages,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'main/messages.html', context)

def paint(request):
    return render(request, 'main/paint.html')

def add_comment(request):
    get_painting = Paintings.objects.get(id=request.POST.get('painting_id'))
    get_comment = request.POST.get('comment')
    new_comment = Comment(painting=get_painting, body=get_comment,
        commenter=request.user)
    new_comment.save()
    return redirect('view_paint', pk=get_painting.id,
        paint=get_painting.slug)


class AddPaintingView(CreateView):
    model = Paintings
    form_class = AddPainting
    template_name = 'main/add_paint.html'

    def form_valid(self, form):
        form.instance.adder = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        global context
        context = super().get_context_data(**kwargs)

        context['unread_count'] = Message.objects.filter(recepient=current_user(self.request), 
            read=False).count()

        return context


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

        context['unread_count'] = Message.objects.filter(recepient=current_user(self.request), 
            read=False).count()
        context['form'] = AddPaintingTry()
        context['similar_paintings'] = painting_list

        return context


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

def save_to_folder(request):
    return HttpResponse(status=204)

def view_folders(request):
    all_folders = Folder.objects.filter(user=request.user)
    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'all_folders': all_folders,
    }
    return render(request, 'main/view_folders.html', context)

def download_painting(request, paint_pk):
    redirect_to = Paintings.objects.get(id=paint_pk)
    # Code to download goes here

    django_messages.success(request, "Paint has been successfully downloaded!")
    return redirect('view_paint', pk=redirect_to.id,
        paint=redirect_to.slug)

def folder_content(request, folder):
    folder_pics = Folder.objects.get(id=folder, user=request.user)
    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'folder_pics': folder_pics.saved_painting.all(),
        'folder_name': folder_pics.name,
        'folder_id': folder_pics.id,
    }
    return render(request, 'main/folder_content.html', context)

def delete_folder(request, folder_pk):
    folder = Folder.objects.get(id=folder_pk, user=request.user)
    folder.delete()
    return redirect('view_folders')

def delete_folder_paint(request):
    to_redirect = request.POST.get('folder_to_redirect')
    return redirect('folder_content', to_redirect)

def save_to_folder(request, paint_pk):
    redirect_to = Paintings.objects.get(id=paint_pk)
    if request.method == 'POST':
        folder = request.POST.get('test')
        print(folder)
        django_messages.success(request, 'Paint saved successfully')
        return redirect('view_paint', pk=redirect_to.id,
            paint=redirect_to.slug)

    context = {
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count(),
        'folders_list': Folder.objects.filter(user=request.user),
        'paint_pk': paint_pk,
    }
    return render(request, 'main/create_or_save.html', context)

def create(request):
    paint_pk = request.POST.get('paint_id')
    name = request.POST.get('name')
    if name:
        Folder.objects.create(user=request.user, name=name)
    else:
        django_messages.warning(request, 'Empty folder name is not allowed')
    return redirect('save_paint', paint_pk)
