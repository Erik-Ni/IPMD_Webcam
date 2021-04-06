import os
from django.conf import settings

def print_data_to_file(time, data):
	with open(settings.EMOTION_FILE, 'a+') as emotion_file:
		print("{} {}".format(str(time), str(data)), file = emotion_file)