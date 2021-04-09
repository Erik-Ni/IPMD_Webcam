from django.apps import AppConfig
from django.conf import settings
import cv2

class FaceDetectorConfig(AppConfig):
	name = 'face_detector'
	net = cv2.dnn.readNetFromCaffe(settings.DEPLOY_PROTOTXT_TXT, settings.RES_CAFFE_MODEL)
