from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartProducts.as_view(), name='cart_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/', views.delete_from_cart, name='delete_from_cart'),
]
