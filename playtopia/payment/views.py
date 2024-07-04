import uuid
import stripe
#
from yookassa import Configuration, Payment
from typing import Any
#
from django.urls import reverse
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#
from django.conf import settings
from cart.cart import CartApp
from store.models import Product
#
from .models import Order, OrderItem
from .services import get_usd_rate
from .key import Key


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

# Create your views here.
class Checkout(LoginRequiredMixin, TemplateView):
    template_name = 'payment/checkout.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = CartApp(self.request)
        context['sum'] = cart.get_total_price()
        return context

class OrdersUser(LoginRequiredMixin, ListView):
    template_name = 'payment/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        for order in orders:
            order.products = [item.product for item in order.items.all()]
        return context


class ShowOrder(LoginRequiredMixin, DetailView):
    template_name = 'payment/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        order = context['order']
        order.products = [item.product for item in order.items.all()]
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        order = Order.objects.get(pk=self.kwargs['id'])
        if order.user != self.request.user:
            raise Http404("Вы не имеете доступа к этому заказу.")
        return order


def complete_order(request: HttpRequest):
    if request.POST:
        cart = CartApp(request)
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')
        user = request.user
        amount = cart.get_total_price()

        order = Order.objects.create(user=user, amount=amount)
        key = Key(order)

        match payment_type:
            case 'stripe-payment':
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment_fail')),
                    'client_reference_id': order.id,
                    'line_items': []
                }

                usd_rate = int(get_usd_rate())

                for item in cart.user_cart:
                    product = Product.objects.get(pk=item.product_id)
                    OrderItem.objects.create(order=order, product=product,
                                            price=product.price, quantity=item.quantity)

                    session_data['line_items'].append({
                        'price_data': {
                            'unit_amount': int((product.price / usd_rate) * 100),
                            'currency': 'usd',
                            'product_data': {
                                'name': product.name
                            }
                        },
                        'quantity': item.quantity
                    })

                session = stripe.checkout.Session.create(**session_data)
                return redirect(session.url, code=303)

            case 'yookassa-payment':
                idempotency_key = uuid.uuid4()
                currency = 'RUB'
                description = 'Товары в корзине'
                payment = Payment.create({
                    'amount': {
                        'value': str(amount),
                        'currency': currency
                    },
                    'confirmation': {
                        'type': 'redirect',
                        'return_url': request.build_absolute_uri(reverse('payment:payment_success'))
                    },
                    'capture': True,
                    'test': True,
                    'description': description

                }, idempotency_key)

                confirmation_url = payment.confirmation.confirmation_url

                for item in cart.user_cart:
                    product = Product.objects.get(pk=item.product_id)
                    OrderItem.objects.create(order=order, product=product,
                                            price=product.price, quantity=item.quantity)
                return redirect(confirmation_url)


@login_required
def payment_success(request: HttpRequest):
    cart = CartApp(request)
    cart.user_cart.all().delete()

    return render(request, 'payment/payment-success.html')

@login_required
def payment_fail(request: HttpRequest):
    return render(request, 'payment/payment-fail.html')
