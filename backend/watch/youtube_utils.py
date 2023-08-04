import requests
from django.conf import settings


def get_youtube_video_info(video_id):
    token = settings.YOUTUBE_API_KEY
    api_path = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id="

    resp = requests.get(api_path + video_id + "&key=" + token)
    data = resp.json()

    return data["items"][0]["snippet"]
