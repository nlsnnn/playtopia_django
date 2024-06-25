from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),

    path('password-change/', views.PasswordChange.as_view(), name='password-change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password-change-done'),

    path('orders/', views.OrdersUser.as_view(), name='orders'),
    path('order/<int:id>', views.ShowOrder.as_view(), name='show_order')
]
