from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from .forms import VideoForm
from .models import Video

class Home(TemplateView):
    template_name = 'index.html'

def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = VideoForm()
    if request.FILES:
        return render(request, 'upload.html', {'form': form, 'video': request.FILES['videofile'].name})
    else:
        return render(request, 'upload.html', {'form': form, 'video': {}})