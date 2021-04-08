import os
from django.conf import settings

def print_data_to_file(time, posted):
	with open(settings.POSTED_FILE, 'a+') as file:
		print("{} {}".format(str(time), str(posted)), file = file)