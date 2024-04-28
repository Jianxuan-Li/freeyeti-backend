from __future__ import unicode_literals
import os
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.conf import settings
from django.contrib.auth.models import User
from .models import ChatRoom
from django.db.models import Q
from .serializer import (
    ChatRoomCreationSerializer,
    ChatRoomListSerializer,
    UserInfoSerializer,
)


class RoomList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get(self, request):
        rooms = (
            ChatRoom.objects.filter(~Q(is_private=True) | Q(user=request.user))
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

        existing_room = ChatRoom.objects.filter(
            slug=serializer.validated_data["slug"]
        ).first()
        if existing_room:
            return Response(
                {"message": "Room with this slug already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        room = ChatRoom.objects.filter(slug=room_id).first()

        if not room:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChatRoomListSerializer(room)

        return Response({"data": serializer.data})

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


class AskJoinRoom(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id):
        room = ChatRoom.objects.filter(slug=room_id).first()

        if not room:
            return Response(
                {"message": "Room not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if room.is_private:
            if not request.data.get("passcode"):
                return Response(
                    {"message": "Passcode is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if room.passcode != request.data.get("passcode"):
                return Response(
                    {"message": "Invalid passcode"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = ChatRoomListSerializer(room)

        return Response(
            {
                "message": "You have joined the room successfully",
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ContactList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserInfoSerializer(users, many=True)

        return Response(
            {
                "data": serializer.data,
                "meta": {"count": len(users)},
            }
        )
