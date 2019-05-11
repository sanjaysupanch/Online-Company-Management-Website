from django.urls import path
from put_calendar import views
from django.conf.urls import url
app_name='put_calendar'
urlpatterns = [






    url(r'^next/(?P<select>\w+)/(?P<show>\w+)/$', views.date, name='date'),
    #path('next/<select>/',views.date,name = "date"),
    #path('back/<select>/',views.date1,name = "date1"),
    url(r'^back/(?P<select>\w+)/(?P<show>\w+)/$', views.date1, name='date1'),
    path('events_enter/<int:date_selected>',views.event_enter,name="event_enter"),
    url(r'^land/(?P<select>\w+)/(?P<show>\w+)/$', views.hello, name='index'),
	url(r'^choose/(?P<select>\w+)/(?P<show>\w+)/$', views.choose_event, name='choose'),


]
