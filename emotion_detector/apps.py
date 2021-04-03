from django.apps import AppConfig
from django.conf import settings
from keras.models import load_model
import os

class EmotionDetectorConfig(AppConfig):
	name = 'emotion_detector'
	MODEL_DIR = os.path.join(settings.BASE_DIR, settings.EMOTION_MODEL)
	model = load_model(MODEL_DIR)