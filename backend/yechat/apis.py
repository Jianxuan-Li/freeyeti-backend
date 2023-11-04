from __future__ import unicode_literals
import os
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conf import settings
from .models import ChatRoom
from django.db.models import Q
from .serializer import ChatRoomCreationSerializer, ChatRoomListSerializer


class RoomList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get(self, request):
        rooms = (
            ChatRoom.objects.filter(Q(user=request.user) | Q(is_private=False))
            .order_by("-updated_at")
            .all()
        )

        serializer = ChatRoomListSerializer(rooms, many=True)

        return Response(
            {
                "data": serializer.data,
                "meta": {"count": len(rooms)},
            }
        )

    def post(self, request):
        serializer = ChatRoomCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room = ChatRoom.objects.create(
            name=serializer.validated_data["name"],
            user=request.user,
            is_private=serializer.validated_data["is_private"],
            passcode=serializer.validated_data["passcode"],
            slug=serializer.validated_data["slug"],
        )
        return Response(
            {"message": "Room created successfully", "data": {"id": room.id}},
            status=status.HTTP_201_CREATED,
        )


class Room(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def delete(self, request, room_id):
        room = ChatRoom.objects.filter(id=room_id, user=request.user).first()

        if not room:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        room.delete()
        return Response(
            {"message": "Room deleted successfully"}, status=status.HTTP_200_OK
        )

    def get(self, request, room_id):
        room = ChatRoom.objects.filter(id=room_id).first()

        if not room:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response({"data": room}, status=status.HTTP_200_OK)

    def put(self, request, room_id):
        room = ChatRoom.objects.filter(id=room_id, user=request.user).first()

        if not room:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatRoomCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        room.name = serializer.validated_data["name"]
        room.is_private = serializer.validated_data["is_private"]
        room.passcode = serializer.validated_data["passcode"]
        room.slug = serializer.validated_data["slug"]
        room.save()
        return Response(
            {"message": "Room updated successfully", "data": room},
            status=status.HTTP_200_OK,
        )
