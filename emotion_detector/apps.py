from django.apps import AppConfig
from django.conf import settings
from tensorflow.keras.models import load_model

class EmotionDetectorConfig(AppConfig):
	name = 'emotion_detector'
	model = load_model(settings.EMOTION_MODEL)
