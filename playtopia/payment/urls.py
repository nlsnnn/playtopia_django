from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('complete-order/', views.complete_order, name='complete_order'),
    path('success/', views.payment_success, name='payment_success'),
    path('fail/', views.payment_fail, name='payment_fail')
]
