from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('<int:id>', views.detail, name="product_detail"),
    path('list', views.product_list, name="product_list"),
    path('category_navbar', views.category_product, name="navbar"),
    path('category', views.category_test, name="category"),
]
