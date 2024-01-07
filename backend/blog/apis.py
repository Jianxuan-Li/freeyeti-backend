from __future__ import unicode_literals
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conf import settings
from .models import LifeBlogPage, BlogPage

video_root = settings.MEDIA_ROOT + "/videos/"
image_ext = ["jpg", "jpeg", "png", "webp"]


class UpdateViewCount(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        blog_type = request.GET.get("type", None)
        blog_id = request.GET.get("id", None)

        if blog_type is None or blog_id is None:
            return Response(
                {"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if blog_type == "blog.LifeBlogPage":
                blog = LifeBlogPage.objects.get(id=blog_id)
            else:
                blog = BlogPage.objects.get(id=blog_id)

            blog.view_count += 1
            blog.save()
        except:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "data": {
                    "view_count": blog.view_count,
                }
            }
        )
