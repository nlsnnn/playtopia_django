from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from store.models import Cart, Product



class CartProducts(ListView):
    template_name = 'cart/products.html'
    model = Cart
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        cart = Cart.objects.filter(user_id=self.request.user)
        product_ids = cart.values_list('product_id', flat=True)
        return Product.objects.filter(id__in=product_ids)



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


def delete_from_cart(request: HttpRequest):
    if request.method ==  'POST':
        product_id = request.POST.get('product_id')
        cart_item = get_object_or_404(Cart, user_id=request.user,
                                      product_id=product_id)
        cart_item.delete()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
