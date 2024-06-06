from decimal import Decimal
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from store.models import Cart, Product


class CartApp:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        self.user = request.user
        self.product_id = request.POST.get('product_id')

    def add_to_cart(self):
        product = get_object_or_404(Product, id=self.product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=self.user, product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True, 'quantity': cart_item.quantity})

    def delete_from_cart(self):
        cart_item = self.get_item_cart()
        p_sum = Product.objects.get(id=self.product_id).price
        cart_item.delete()

        return JsonResponse({'success': True, 'sum': p_sum})

    def add_item_cart(self):
        cart_item: Cart = self.get_item_cart()

        new_quantity = int(cart_item.quantity) + 1
        cart_item.quantity = new_quantity
        cart_item.save()

        return JsonResponse({'success': True, 'quantity': new_quantity})

    def sub_item_cart(self):
        cart_item: Cart = self.get_item_cart()

        last = False
        quantity = cart_item.quantity
        if cart_item.quantity > 1:
            cart_item.quantity = quantity - 1
            cart_item.save()
        else:
            cart_item.delete()
            last = True

        return JsonResponse({'success': True, 'quantity': quantity-1, 'last': last})


    def get_item_cart(self):
        return get_object_or_404(Cart, user_id=self.user, product_id=self.product_id)
