from django.conf.urls import url
from . import views

app_name = 'clients'

urlpatterns = [
    #clients
    url('^$', views.index, name='index'),

    #clients/create/
    url('create/', views.client_create_view,name='create')
]