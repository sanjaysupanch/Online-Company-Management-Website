from django.conf.urls import url
from django.urls import path


from chat import views


urlpatterns = [
    path('chat/<int:pk>/',views.index,name='chat.group'),
]
