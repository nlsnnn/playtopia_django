from django.urls import path, reverse_lazy
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

    path('password-reset/', views.PasswordResetView.as_view(
        template_name='users/reset/password_reset_form.html',
        email_template_name='users/reset/password_reset_email.html',
        success_url=reverse_lazy('users:password-reset-done')
    ), name='password-reset'),

    path('password-reset/done/', views.PasswordResetDoneView.as_view(
        template_name='users/reset/password_reset_done.html'
    ), name='password-reset-done'),

    path('password-reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='users/reset/password_reset_confirm.html',
        success_url=reverse_lazy('users:password-reset-complete')
    ), name='password-reset-confirm'),

    path('password-reset/complete/', views.PasswordResetCompleteView.as_view(
        template_name='users/reset/password_reset_complete.html'
    ), name='password-reset-complete'),

    path('orders/', views.OrdersUser.as_view(), name='orders'),
    path('order/<int:id>', views.ShowOrder.as_view(), name='show_order')
]
