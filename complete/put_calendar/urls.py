from django.urls import path
from put_calendar import views
app_name='put_calendar'
urlpatterns = [
  path('next/',views.date,name = "date"),
  path('back/',views.date1,name = "date1"),
  path('',views.hello,name="index"),
  path('create_events/',views.create_event,name='events'),
  path('create_group/',views.create_group,name='groups'),
  path('group_next/',views.group_date,name='group_date'),
  path('group_back/',views.group_date1,name='group_date1'),
  path('group/',views.group_hello,name='group_index'),
]
