import stripe

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe.error

from .tasks import send_order_confirmation
from .models import Order


@csrf_exempt
def stripe_webhook(request: HttpRequest):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order_id = session.client_reference_id
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            send_order_confirmation.delay(order_id)
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

    return HttpResponse(status=200)
