

from django.conf.urls import url
from django.urls import path
from .views import *


#app_name='blog'
urlpatterns = [
    path('rest/<int:pk>/', BlogPostRudView.as_view() , name='post-rud'),


    ]
