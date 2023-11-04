from django.urls import path
from backend.yechat.apis import RoomList, Room

urlpatterns = [
    path("", RoomList.as_view(), name="chat-room-list"),
    path("<str:room_id>/", Room.as_view(), name="chat-room"),
]
