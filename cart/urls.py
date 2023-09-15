from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail', views.cart_detail, name="cart_detail"),
    path('add/<int:pk>', views.cart_add, name="cart_add"),
    path('delete/<str:id>', views.cart_delete, name="cart_delete"),
    path('order/<int:pk>', views.order_detail, name="order_detail"),
    path('order/create', views.order_create, name="order_create"),
    path('sendrequest/<int:pk>', views.send_request, name="send_request"),
    path('verify', views.verify, name="verify_request"),
]
