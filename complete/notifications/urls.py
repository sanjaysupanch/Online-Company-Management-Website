from django.conf.urls import url
from . import views

app_name = 'notifications'

urlpatterns = [
    #notifications
    url('^$', views.index, name='index'),

    url('update/(?P<notify_id>[0-9]+)', views.update, name='update'),

]