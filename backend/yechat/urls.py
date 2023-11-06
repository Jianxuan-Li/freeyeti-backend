from django.urls import path
from backend.yechat.apis import RoomList, Room, AskJoinRoom

urlpatterns = [
    path("", RoomList.as_view(), name="chat-room-list"),
    path("<slug:room_id>/", Room.as_view(), name="chat-room"),
    path("<slug:room_id>/join/", AskJoinRoom.as_view(), name="chat-room-join"),
]
