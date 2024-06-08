from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import UpdateView

from cart.cart import CartApp
from store.models import Product

from .models import Order, OrderItem
from .forms import CheckoutForm


# Create your views here.
class Checkout(UpdateView):
    form_class = CheckoutForm
    template_name = 'payment/checkout.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = CartApp(self.request)
        context['sum'] = cart.get_total_price()
        return context


def complete_order(request: HttpRequest):
    if request.POST.get('action') == 'payment':
        user = request.user
        amount = request.POST.get('amount')
        cart = CartApp(request)

        order = Order.objects.create(user=user, amount=amount)

        for item in cart.user_cart:
            product = Product.objects.get(pk=item.product_id)
            OrderItem.objects.create(order=order, product=product,
                                     price=product.price, quantity=item.quantity)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def payment_success(request: HttpRequest):
    cart = CartApp(request)
    cart.user_cart.all().delete()

    return render(request, 'payment/payment-success.html')

def payment_fail(request: HttpRequest):
    return render(request, 'payment/payment-fail.html')
