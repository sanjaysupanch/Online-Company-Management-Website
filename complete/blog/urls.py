from django.conf.urls import url
from django.urls import path
from blog import views

#app_name='blog'
urlpatterns = [
    path('show/<int:pk>/', views.index, name='blog_index'),
    #url(r'^show/(?P<pk>\d+)/$',views.index,name='blog_index'),
    path('post/<int:pk>/', views.details, name='details'),
    path('post/new/<int:pk>/', views.newpost, name='newpost'),
    path('post/<int:pk>/edit', views.editpost, name='editpost'),
    path('post/<int:pk>/delete', views.deletepost, name='deletepost'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.addcomment, name='add-comment'),
]
