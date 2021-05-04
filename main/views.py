from django.shortcuts import render, redirect
from .forms import AddPainting
from django.views.generic import ListView, CreateView, DetailView
from .models import Paintings


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

class IndexListView(ListView):
    model = Paintings
    template_name = 'main/index.html'

def notifications(request):
    return render(request, 'main/notifications.html')

def messages(request):
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


