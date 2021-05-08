from django.shortcuts import render, redirect
from .forms import AddPainting
from django.views.generic import ListView, CreateView, DetailView
from .models import Paintings, Message
from users.models import CustomUser
from django.contrib import messages as django_messages


class IndexListView(ListView):
    model = Paintings
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        global context
        context = super().get_context_data(**kwargs)


        if self.request.user.is_authenticated:
            unread_messages = Message.objects.filter(recepient=self.request.user, read_or_not=False)
            context['unread_count'] = unread_messages.count()

        return context
        


def messages(request):
    receiver = request.POST.get('painter_name')
    message = request.POST.get('message')
    painter = CustomUser.objects.filter(username=receiver).first()
    Message.objects.create(sender=request.user, recepient=painter, message=message)
    django_messages.success(request, "Message sent successfully.")
    return redirect('painter_profile', painter=receiver)

def notifications(request):
    return render(request, 'main/notifications.html')

def view_messages(request):
    return render(request, 'main/messages.html')

def paint(request):
    return render(request, 'main/paint.html')


class AddPaintingView(CreateView):
    model = Paintings
    form_class = AddPainting
    template_name = 'main/add_paint.html'

    def form_valid(self, form):
        form.instance.adder = self.request.user
        return super().form_valid(form)


class PaintingDetailView(DetailView):
    model = Paintings
    template_name = 'main/view_paint.html'


