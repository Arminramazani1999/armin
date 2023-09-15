from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.user_login, name="login"),
    path('register', views.user_register, name="register"),
    path('logout', views.user_logout, name="logout"),
    path('otplogin', views.otp_login, name="otp_login"),
    path('checked', views.user_check_cod, name="checked"),
    path('address', views.address_add, name="address_add"),
]

