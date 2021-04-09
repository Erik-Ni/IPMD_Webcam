from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from collections import defaultdict
import cv2
import os
import threading

from .forms import VideoForm
from .models import Video
from modules.video_analysis import video_analysis
from modules.load_data_to_posted import load_data_to_posted

import threading

class Home(TemplateView):
	template_name = 'index.html'

class Analysis(object):
	def __init__(self, video_filename):
		self.folder_dir = settings.MEDIA_URL
		self.video_filename = video_filename
		self.out_video_filename = '{}_result.mp4'.format(video_filename.split('.')[0])
		self.out_posted_filename = '{}_posted.csv'.format(video_filename.split('.')[0])
		self.video_dir = ".{}{}".format(self.folder_dir, self.video_filename)
		self.out_video_dir = ".{}{}".format(self.folder_dir, self.out_video_filename)
		self.out_posted_dir = ".{}{}".format(self.folder_dir, self.out_posted_filename)

		self.posted = defaultdict(lambda : dict)
		threading.Thread(target = self.update, args=()).start()

	def update(self):
		all_data = video_analysis(self.video_dir, self.out_video_dir)
		load_data_to_posted(all_data, self.posted)

		with open(self.out_posted_dir, 'w') as file:
			print(self.posted, file = file)

def upload(request):
	if request.method == 'POST':
		print(request.POST, request.FILES)
		form = VideoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
	else:
		form = VideoForm()

	if request.FILES:
		video_filename = request.FILES['videofile'].name

		analysis = Analysis(video_filename)

		# analysis.posted for data analyzation after calculated by thread

		return render(request, 'upload.html', {'form': form, 'video': analysis.video_filename})
	else:
		return render(request, 'upload.html', {'form': form, 'video': {}})
