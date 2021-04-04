from django.shortcuts import render,redirect

from .models import Videos

# Create your views here.

def upload_video(request):

    if request.method == 'POST':

        title = request.POST['title']
        video = request.POST['video']

        content = Videos(title=title,video=video)
        content.save()
        return redirect('home')

    return render(request,'upload.html')


def display(request):

    videos = Videos.objects.all()
    context ={
        'videos':videos,
    }

    return render(request,'videos.html',context)
