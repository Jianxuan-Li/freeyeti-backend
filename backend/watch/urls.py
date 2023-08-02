from django.urls import path
from backend.watch.apis import WatchList, Video

urlpatterns = [
    path("", WatchList.as_view(), name="watch-index"),
    path("<slug:video_id>/", Video.as_view(), name="watch-video"),
]