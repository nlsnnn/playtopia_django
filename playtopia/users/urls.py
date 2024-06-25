from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('orders/', views.OrdersUser.as_view(), name='orders'),
    path('order/<int:id>', views.ShowOrder.as_view(), name='show_order')
]
