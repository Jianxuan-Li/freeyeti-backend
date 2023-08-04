from __future__ import unicode_literals
import os
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conf import settings
import youtube_dl
from .youtube_utils import get_youtube_video_info
from .models import Watch

video_root = settings.MEDIA_ROOT + "/videos/"
image_ext = ["jpg", "jpeg", "png", "webp"]


class WatchList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get(self, request):
        if not os.path.exists(video_root):
            os.makedirs(video_root)

        videos = Watch.objects.filter(user=request.user).order_by("-created_at").all()
        data = []

        for video in videos:
            info = {
                "title": video.title,
                "videoId": video.video_id,
                "url": settings.MEDIA_URL + "videos/" + video.video_id + ".mp4",
            }

            for ext in image_ext:
                if os.path.exists(video_root + video.video_id + "." + ext):
                    info["thumbnail"] = (
                        settings.MEDIA_URL + "videos/" + video.video_id + "." + ext
                    )
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
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def post(self, request, video_id):
        if not re.match(r"([a-zA-Z0-9_-]{11})", video_id):
            return Response(
                {"message": "Invalid video id"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            video_info = get_youtube_video_info(video_id)
        except:
            return Response(
                {"message": "Video info not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if Watch.objects.filter(video_id=video_id).exists():
            if Watch.objects.filter(video_id=video_id, user=request.user).exists():
                return Response(
                    {"message": "Video already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Watch.objects.create(
                title=video_info["title"],
                video_id=video_id,
                user=request.user,
            )
            return Response(
                {"message": "Video already exists, copied"}, status=status.HTTP_200_OK
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

        for ext in image_ext:
            if os.path.exists(video_root + video_id + "." + ext):
                break

        Watch.objects.create(
            title=video_info["title"],
            video_id=video_id,
            user=request.user,
        )

        return Response({"message": "Video uploaded successfully"})

    def delete(self, request, video_id):
        if not re.match(r"([a-zA-Z0-9_-]{11})", video_id):
            return Response(
                {"message": "Invalid video id"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not Watch.objects.filter(video_id=video_id).exists():
            return Response(
                {"message": "Video does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not Watch.objects.filter(video_id=video_id, user=request.user).exists():
            return Response(
                {"message": "You are not allowed to delete this video"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Watch.objects.filter(video_id=video_id).count() == 1:
            video_path = video_root + video_id + ".mp4"
            if os.path.exists(video_path):
                os.remove(video_path)

            for ext in image_ext:
                if os.path.exists(video_root + video_id + "." + ext):
                    os.remove(video_root + video_id + "." + ext)
                    break

        Watch.objects.filter(video_id=video_id, user=request.user).delete()

        return Response(
            {"message": "Video deleted successfully"}, status=status.HTTP_200_OK
        )
