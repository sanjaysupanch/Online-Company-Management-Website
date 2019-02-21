from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room,Chat

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from .serializers import ChatModelSerializer

from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

from accounts.models import teamtable

@login_required
def index(request,pk):

    if pk:


        team=teamtable.objects.get(pk=pk)
        room = Room.objects.get(teamdetails=team)

        rooms=[]
        rooms.append(room)


        return render(request, "index.html", {
            "rooms": rooms,
        })

class ChatModelViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.filter(Q(pk=kwargs['pk']))
        return super(ChatModelViewSet, self).list(request, *args, **kwargs)
