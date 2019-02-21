from django.conf.urls import url
from history import views
from django.urls import path

app_name = 'history'

urlpatterns = [
 url('activity/',views.trials,name = 'trials'),
]
