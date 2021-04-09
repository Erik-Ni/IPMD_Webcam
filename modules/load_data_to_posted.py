from django.conf import settings
from collections import defaultdict

emotions = settings.EMOTION_LISTS
moods = settings.MOOD_LISTS

def load_data_to_posted(all_data, posted):
	emotion_avg, emotion_freq, mood_avg, mood_freq = {}, {}, {}, {}

	for i in range(len(emotions)):
		if all_data["count"][0] >= 1.00:
			emotion_avg[emotions[i]] = int(round(all_data[emotions[i]][0] / all_data["count"][0], 2) * 100)
		else:
			emotion_avg[emotions[i]] = 0

		if all_data["count"][1] >= 1.00:
			emotion_freq[emotions[i]] = int(round(all_data[emotions[i]][1] / all_data["count"][1], 2) * 100)
		else:
			emotion_freq[emotions[i]] = 0

	for i in range(len(moods)):
		if all_data["count"][2] >= 1.00:
			mood_avg[moods[i]] = int(round(all_data[moods[i]][2] / all_data["count"][2], 2) * 100)
		else:
			mood_avg[moods[i]] = 0

		if all_data["count"][3] >= 1.00:
			mood_freq[moods[i]] = int(round(all_data[moods[i]][3] / all_data["count"][3], 2) * 100)
		else:
			mood_freq[moods[i]] = 0

	posted["emotion_avg"] = emotion_avg
	posted["emotion_freq"] = emotion_freq
	posted["mood_avg"] = mood_avg
	posted["mood_freq"] = mood_freq
	
	all_data = defaultdict(lambda : [0.00, 0.00, 0.00, 0.00])