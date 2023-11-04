from rest_framework import serializers
from .models import ChatRoom
from django.contrib.auth.models import User


class ChatRoomCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    is_private = serializers.BooleanField(default=False)
    passcode = serializers.CharField(max_length=20, allow_blank=True, allow_null=True)
    slug = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
        ]


class ChatRoomListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    user = UserInfoSerializer(read_only=True)
    is_private = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "name",
            "slug",
            "user",
            "is_private",
            "created_at",
            "updated_at",
        ]
