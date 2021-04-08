from django.apps import AppConfig
from django.conf import settings
from tensorflow.keras.models import load_model

class MoodDetectorConfig(AppConfig):
	name = 'mood_detector'
	model = load_model(settings.MOOD_MODEL)
