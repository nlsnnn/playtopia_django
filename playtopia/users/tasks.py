from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_registration_mail(user, email):
    subject, from_email, to = "Регистрация на Playtopia", settings.EMAIL_HOST_USER, email
    html_content = render_to_string('email/registration_email.html', {'user': user})
    msg = EmailMultiAlternatives(subject, from_email=from_email, to=[to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
