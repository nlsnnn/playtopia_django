from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from .models import Order

@shared_task
def send_order_confirmation(order_id, email):
    order = Order.objects.get(pk=order_id)
    amount = order.amount
    subject = f'Заказ {order_id}'
    from_email = settings.EMAIL_HOST_USER
    message = f'Ваш заказ подтвержден.\nID заказа - {order_id}'

    mail_to_sender = send_mail(
        subject, message, from_email, recipient_list=[email],
    )
    return mail_to_sender
