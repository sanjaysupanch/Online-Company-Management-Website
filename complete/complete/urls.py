from django.contrib import admin
from django.conf.urls import include, url
from accounts.views import home
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chat.views import index

from put_calendar.api.router import router

from put_calendar.views import *


from rest_framework.authtoken import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('assignments/', include('assignments.urls')),
    url('notifications/', include('notifications.urls')),
    url('clients/', include('clients.urls')),
    url('accounts/',include('accounts.urls')),
    url('history/', include('history.urls')),
    url('^$',home),
    url('blog/', include('blog.urls')),
    url('calendar/',include('put_calendar.urls')),
    url('chat/',include('chat.urls')),
    url('api/posts/',include('blog.api.urls')),
    path('api/',include(router.urls)),
    path('api-token-auth/',views.obtain_auth_token,name='api-token-auth'),


    url(r'^api/dates/$', DatesListView.as_view()),
    url(r'^api/dates/(?P<pk>\d+)/$', DatesView.as_view()),
    url(r'^api/user/$', UserListView.as_view()),
    url(r'^api/user/(?P<pk>\d+)/$', UserView.as_view()),
    url(r'^api/filter/(?P<pk>\d+)/$', DatesFilterView.as_view()),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
