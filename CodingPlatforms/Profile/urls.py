from django.contrib import admin
from django.urls import path
from Profile import views

urlpatterns = [
    #path("", views.index, name='firstpage'),
    path('' ,  views.home  , name="home"),
    path('register' , views.register_attempt , name="register_attempt"),
    path('accounts/login/' , views.login_attempt , name="login_attempt"),
    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
    path('ResetPassword', views.ResetPass, name="ResetPass"),
    path('change_password/<auth_token>', views.change_password, name="change_password"),
    path('edit_profile/<str:username>', views.edit_profile, name="edit_profile"),
    path('view_profile/<str:username>', views.view_profile, name="view_profile"),
]