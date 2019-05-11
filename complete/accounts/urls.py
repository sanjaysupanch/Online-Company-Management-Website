from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

#app_name='accounts'

urlpatterns=[
        path('index/',views.index, name='index'),
        path('',views.home,name='home'),
        path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'), #login url
        path('logout/',auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),  #logout url
        path('register/',views.register,name='register'),             #register url
        path('register/company',views.registercompany,name='registercompany'),             #register url
        path('profile/',views.view_profile,name='view_profile'),
        path('profile/edit/',views.edit_profile,name='edit_profile'),
        path('profile/password/',views.change_password,name='change_password'),
        path('change-password/',views.change_password,name='change_password'), #change password url
        path('recent_activities/',views.list_activities,name='list_activities'),
        path('employee_activity/<int:pk>/',views.specific_activities,name='specific_activities'),
        path('inter_reg/',views.inter_reg,name='inter_reg'),

        path('reset-password/',auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'
        ,email_template_name = 'accounts/reset_password_email.html'),name='password_reset'), # password reset url
        # password reset done url
        path('reset-password/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'),
        name='password_reset_done'),
        #password reset confirm url
        path('reset-password/confirm/(<uidb64>[0-9A-Za-z]+)-(<token>.+)/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'),
        name='password_reset_confirm'),
        #password reset complete url
        path('reset-password/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'),name='password_reset_complete'),
        #path('reset/real', include('django.contrib.auth.urls')),

        url(r'^profile/(?P<pk>\d+)/$',views.view_profile,name='view_profile_with_pk'),

        path('createteam/',views.create_team,name='reg_team'),
        path('addusertoteam/',views.add_user_team,name='add_user_team'),
        path('todolists/<int:pk>/',views.todo,name='accounts.todo'),
        path('group/<int:pk>/',views.view_group_with_pk,name='view_group_with_pk'),
        path('uploadfilepath/<int:pk>/',views.fileupload,name='file_upload'),
        path('filedownload/<int:pk>/',views.filedownload,name='file_download'),


]
