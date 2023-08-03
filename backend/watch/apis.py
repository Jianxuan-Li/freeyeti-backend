from __future__ import unicode_literals
import os
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conf import settings
import youtube_dl

video_root = settings.MEDIA_ROOT + "/videos/"
image_ext = ["jpg", "jpeg", "png", "webp"]


class WatchList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get(self, request):
        if not os.path.exists(video_root):
            os.makedirs(video_root)

        videos = os.listdir(video_root)

        data = []

        for video in videos:
            name, ext = video.split(".")[0], video.split(".")[1]
            if ext != "mp4":
                continue

            info = {
                "title": video.split(".")[0],
                "url": settings.MEDIA_URL + "videos/" + video,
            }

            for ext in image_ext:
                if os.path.exists(video_root + name + "." + ext):
                    info["thumbnail"] = settings.MEDIA_URL + "videos/" + name + "." + ext
                    break
            data.append(info)

        return Response(
            {
                "data": data,
                "meta": {"count": len(data), "media_url": settings.MEDIA_URL},
            }
        )


class Video(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = []

    def post(self, request, video_id):
        # test video_id matchs (.*?)(^|\/|v=)([a-z0-9_-]{11})(.*)?
        if not re.match(r"([a-zA-Z0-9_-]{11})", video_id):
            return Response(
                {"message": "Invalid video id"}, status=status.HTTP_400_BAD_REQUEST
            )

        video_path = video_root + video_id + ".mp4"

        if os.path.exists(video_path):
            os.remove(video_path)

        ydl_opts = {
            "outtmpl": video_path,
            "format": "mp4",
            "writethumbnail": True,
        }
        url = "https://www.youtube.com/watch?v=" + video_id
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return Response({"message": "Video uploaded successfully"})

    def delete(self, request, video_id):
        video_path = video_root + video_id + ".mp4"
        thumbnail_path = video_root + video_id + ".webp"

        if os.path.exists(video_path):
            os.remove(video_path)

        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        return Response(
            {"message": "Video deleted successfully"}, status=status.HTTP_200_OK
        )
