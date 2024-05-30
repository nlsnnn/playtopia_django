from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from store.models import Cart, Product



def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True, 'quantity': cart_item.quantity})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
