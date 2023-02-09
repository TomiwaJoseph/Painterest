from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddPainting, AddPaintingTry
from django.views.generic import DetailView
from .models import Paintings, Message, Comment, Folder
from users.models import CustomUser, Profile, UserFollowing
from django.contrib import messages as django_messages
import random
from django.db.models import Count
from taggit.models import Tag
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse, Http404
from actions.utils import create_action
from actions.models import Action
from django.core.mail import send_mail
from django.conf import settings


# GLOBAL VARIABLES
no_category_selected = []
auth_all_painting = []
all_similar_paintings = []
all_actions = []


# Ajax requests starts here


def notification_fetch(request):
    each_load = request.GET.get('each_load')
    start_from = request.GET.get('start_from')

    # Display all followings
    following_ids = request.user.following.values_list('id',
                                                       flat=True)

    if following_ids:
        # If user is following others, retrieve only specified amount of actions
        actions = all_actions[int(start_from):int(start_from) + int(each_load)]
    else:
        actions = None

    context = {
        'actions': actions,
    }

    return render(request, 'main/more_notifications.html', context)


def similar_fetch(request, pk, paint):
    each_load = request.GET.get('each_load')
    start_from = request.GET.get('start_from')

    similar_paintings = all_similar_paintings[int(
        start_from):int(start_from) + int(each_load)]
    context = {
        'similar_paintings': similar_paintings,
    }

    return render(request, 'main/similar_paintings.html', context)


def category_fetch(request):
    each_load = request.GET.get('each_load')
    start_from = request.GET.get('start_from')

    if request.user.is_authenticated:
        logged_user = Profile.objects.get(user=request.user).feed_tuner.all()
        all_slugs = [i.slug for i in logged_user]
        if not all_slugs:
            painting_list = no_category_selected[int(
                start_from):int(start_from) + int(each_load)]
        else:
            painting_list = auth_all_painting[int(
                start_from):int(start_from) + int(each_load)]
    else:
        painting_list = no_category_selected[int(
            start_from):int(start_from) + int(each_load)]

    context = {
        'object_list': painting_list,
    }

    return render(request, 'main/more_index_pics.html', context)


def mark_single_as_read(request):
    notif_id = request.GET.get('notif_id')
    get_notif = Action.objects.get(id=notif_id)
    get_notif.read = True
    get_notif.save()
    return HttpResponse('Success')


def mark_all_as_read(request):
    for notifications in all_actions:
        notifications.read = True
        notifications.save()
    return HttpResponse('Success')


# Ajax requests ends here


def index(request):
    global no_category_selected, auth_all_painting
    context = {}

    if request.user.is_authenticated:
        logged_user = Profile.objects.get(user=request.user).feed_tuner.all()
        all_slugs = [i.slug for i in logged_user]
        if not all_slugs:
            no_category_selected = list(Paintings.objects.all())
            random.shuffle(no_category_selected)
        else:
            auth_all_painting = []

            for i in range(len(all_slugs)):
                tagg = get_object_or_404(Tag, slug=all_slugs[i])
                object_list = Paintings.objects.filter(tags__in=[tagg]).all()
                auth_all_painting.extend(list(object_list))

            # Shuffle all the user's feeds category paintings
            random.shuffle(auth_all_painting)

        context = {
            'unread_count': Message.objects.filter(recepient=request.user, read=False).count(),
            'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                               flat=True), action_for=request.user, read=False))
        }
    else:
        no_category_selected = list(Paintings.objects.all())
        random.shuffle(no_category_selected)
    return render(request, 'main/index.html', context)


def about(request):
    context = {}
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                                     flat=True), action_for=request.user, read=False))
        context['unread_count'] = Message.objects.filter(recepient=request.user,
                                                         read=False).count()

    return render(request, 'main/about.html', context)


def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            send_mail(subject, message, email,
                      [settings.EMAIL_HOST_USER], fail_silently=False)
            django_messages.success(request, 'Message sent successfully')
        except Exception as e:
            django_messages.error(request, 'Message not sent. Try again.')

        return redirect('contact')

    context = {}
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                                     flat=True), action_for=request.user, read=False))
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
                                                                                           flat=True), action_for=request.user, read=False)),
        'single_message': get_message,
        'unread_count': Message.objects.filter(recepient=request.user,
                                               read=False).count()
    }
    return render(request, 'main/single_message.html', context)


@login_required
def send_message(request):
    receiver = request.POST.get('painter_name')
    message = request.POST.get('message')
    subject = request.POST.get('subject')
    try:
        painter = CustomUser.objects.filter(username=receiver).first()
        Message.objects.create(sender=request.user,
                               recepient=painter, message=message, subject=subject)
        django_messages.success(request, "Message sent successfully.")
        return redirect('painter_profile', painter=receiver)
    except:
        django_messages.error(request, "Message not sent successfully.")
        return redirect('profile')


@login_required
def notifications(request):
    global all_actions
    all_actions = Action.objects.filter(action_for=request.user,
                                        user_id__in=request.user.following.values_list('id',
                                                                                       flat=True))
    signify = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                       flat=True), action_for=request.user, read=False))

    context = {
        'unread_count': Message.objects.filter(recepient=request.user,
                                               read=False).count(),
        'signify': signify,
    }
    return render(request, 'main/notifications.html', context)


@login_required
def view_messages(request):
    all_messages = Message.objects.filter(recepient=request.user)
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                           flat=True), action_for=request.user, read=False)),
        'all_messages': all_messages,
        'unread_count': Message.objects.filter(recepient=request.user,
                                               read=False).count()
    }
    return render(request, 'main/messages.html', context)


@login_required
def add_comment(request):
    get_painting = Paintings.objects.get(id=request.POST.get('painting_id'))
    get_comment = request.POST.get('comment')
    new_comment = Comment(painting=get_painting, body=get_comment,
                          commenter=request.user)
    new_comment.save()
    all_followers = UserFollowing.objects.filter(user_to=CustomUser.objects.filter(
        username=request.user.username).first())
    for user in all_followers:
        create_action(request.user, 'commented on',
                      get_painting, user.user_from)

    return redirect('view_paint', pk=get_painting.id,
                    paint=get_painting.slug)


class PaintingDetailView(DetailView):
    model = Paintings
    template_name = 'main/view_paint.html'

    def get_context_data(self, **kwargs):
        global all_similar_paintings
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

        all_similar_paintings = list(similar_paintings)
        random.shuffle(all_similar_paintings)

        if self.request.user.is_authenticated:
            context['notify'] = len(Action.objects.filter(user_id__in=self.request.user.following.values_list('id',
                                                                                                              flat=True), action_for=self.request.user, read=False))
            context['unread_count'] = Message.objects.filter(recepient=self.request.user,
                                                             read=False).count()

        context['similar_paintings'] = all_similar_paintings
        context['form'] = AddPaintingTry()

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
                                                                                           flat=True), action_for=request.user, read=False)),
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
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


@login_required
def folder_content(request, folder):
    folder_pics = Folder.objects.get(id=folder, user=request.user)
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                           flat=True), action_for=request.user, read=False)),
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
                                                                                           flat=True), action_for=request.user, read=False)),
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
            new_paint.adder = request.user
            new_paint.save()
            all_followers = UserFollowing.objects.filter(user_to=CustomUser.objects.filter(
                username=request.user.username).first())
            for user in all_followers:
                create_action(request.user, 'added', new_paint, user.user_from)
            return redirect(new_paint.get_absolute_url())

    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
                                                                                           flat=True), action_for=request.user, read=False)),
        'form': form,
        'unread_count': Message.objects.filter(recepient=request.user,
                                               read=False).count(),
    }
    return render(request, 'main/add_paint.html', context)
