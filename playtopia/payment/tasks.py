from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from .models import Order

@shared_task
def send_order_confirmation(order_id):
    order: Order = Order.objects.get(id=order_id)
    client = get_user_model().objects.get(id=order.user_id)
    subject = f'Заказ {order_id}'
    from_email = settings.EMAIL_HOST_USER
    recipient = client.email
    message = f'Ваш заказ подтвержден.\nID заказа - {order_id}'

    mail_to_sender = send_mail(
        subject, message, from_email, recipient_list=[recipient],
    )
    return mail_to_sender
