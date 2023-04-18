from rest_framework import serializers

from .models import UserProfile, Rooms, Message
from django.contrib.auth.models import User


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'about', 'rooms', 'avatar',)


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
