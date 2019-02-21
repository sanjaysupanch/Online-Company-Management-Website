from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import Chat
from rest_framework.serializers import ModelSerializer, CharField


class ChatModelSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'user', 'group', 'body','time')
