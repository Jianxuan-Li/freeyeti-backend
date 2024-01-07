from django.urls import path
from backend.blog.apis import UpdateViewCount

urlpatterns = [
    path("view_count/", UpdateViewCount.as_view(), name="update_view_count"),
]