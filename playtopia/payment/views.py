from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import UpdateView

from cart.cart import CartApp

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
