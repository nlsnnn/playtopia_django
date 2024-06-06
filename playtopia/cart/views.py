from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.views.generic import ListView

from store.models import Cart, Product
from .cart import CartApp



class CartProducts(ListView):
    template_name = 'cart/products.html'
    model = Cart
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = CartApp(self.request)
        cart_items = cart.user_cart # Cart.objects.filter(user_id=self.request.user)
        product_quantities = {item.product_id: item.quantity for item in cart_items}

        context['product_quantities'] = product_quantities
        context['amount'] = cart.get_total_price()
        return context

    def get_queryset(self) -> QuerySet[Any]:
        cart = CartApp(self.request).user_cart
        product_ids = cart.values_list('product_id', flat=True)
        return Product.objects.filter(id__in=product_ids)



def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = CartApp(request)
        return cart.add_to_cart()
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def delete_from_cart(request: HttpRequest):
    if request.method ==  'POST':
        cart = CartApp(request)
        return cart.delete_from_cart()
    return JsonResponse({'success': False})


def sub_item_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = CartApp(request)
        return cart.sub_item_cart()
    return JsonResponse({'success': False})


def add_item_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = CartApp(request)
        return cart.add_item_cart()
    return JsonResponse({'success': False})
