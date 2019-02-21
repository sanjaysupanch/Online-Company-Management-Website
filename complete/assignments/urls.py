from django.conf.urls import url
from . import views

app_name = 'assignments'




urlpatterns = [
    #assignments


    #assignments/display
    url('display/$',views.display_view, name='display'),

    #assignments/my_todo
    url('my_todo/$',views.my_todo_view, name='my_todo'),

    #assignments/display/delete
    url('display/delete/(?P<task_id>[0-9]+)',views.delete_tasks,name='delete_task'),

    # assignments/display/update
    url('display/update/(?P<task_id>[0-9]+)', views.update_tasks, name='update_task'),

    #assignments/my_todo/add
    url('my_todo/add/', views.add_todo_list_view, name='add_todo'),

    url('my_todo/delete/(?P<todo_id>[0-9]+)', views.delete_todo, name='delete_todo'),

    url('my_todo/update/(?P<todo_id>[0-9]+)', views.update_todo, name='update_todo'),

]