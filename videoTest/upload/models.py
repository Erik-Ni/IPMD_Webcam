from django.db import models

class Video(models.Model):
	videofile = models.FileField(upload_to = '', null = True, verbose_name = "")

	def __str__(self):
		return str(self.videofile)