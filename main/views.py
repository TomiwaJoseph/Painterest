from django.shortcuts import render, redirect
from .forms import AddPainting, AddPaintingTry
from django.views.generic import ListView, CreateView, DetailView
from .models import Paintings, Message, Comment, PaintTries
from users.models import CustomUser
from django.urls import reverse
from django.contrib import messages as django_messages
import random


def current_user(request):
    user = request.user
    return user

class IndexListView(ListView):
    model = Paintings
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        global context
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['unread_count'] = Message.objects.filter(recepient=self.request.user, read=False).count()

        return context

    def get_queryset(self):
        painting_list = list(Paintings.objects.all())
        painting_list = random.sample(painting_list, 10)
        return painting_list
        

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
    return redirect('messages')

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

def messages(request):
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
        global context
        context = super().get_context_data(**kwargs)

        context['unread_count'] = Message.objects.filter(recepient=current_user(self.request), 
            read=False).count()
        context['form'] = AddPaintingTry()

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