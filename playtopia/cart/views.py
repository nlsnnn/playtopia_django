from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import ListView

from store.models import Cart, Product



class CartProducts(ListView):
    template_name = 'cart/products.html'
    model = Cart
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart_items = Cart.objects.filter(user_id=self.request.user)
        # products: QuerySet = context['products']
        product_quantities = {item.product_id: item.quantity for item in cart_items}
        context['product_quantities'] = product_quantities
        context['amount'] = cart_items.aggregate(total_price=Sum('product__price', field="product__price * quantity")).get('total_price')
        return context

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
        p_sum = Product.objects.get(id=product_id).price
        cart_item.delete()

        return JsonResponse({'success': True, 'sum': p_sum})
    return JsonResponse({'success': False})


def sub_item_cart(request: HttpRequest):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart_item = get_object_or_404(Cart, user_id=request.user,
                                      product_id=product_id)

        quantity = cart_item.quantity
        if (quantity == 1):
            cart_item.delete()
        else:
            cart_item.quantity = quantity - 1
        cart_item.save()

        return JsonResponse({'success': True, 'quantity': quantity-1})
    return JsonResponse({'success': False})


def add_item_cart(request: HttpRequest):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart_item: Cart = get_object_or_404(Cart, user_id=request.user,
                                      product_id=product_id)


        new_quantity = int(cart_item.quantity) + 1
        cart_item.quantity = new_quantity
        cart_item.save()

        return JsonResponse({'success': True, 'quantity': new_quantity})
    return JsonResponse({'success': False})
