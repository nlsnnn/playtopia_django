from decimal import Decimal
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F

from store.models import Cart, Product


class CartApp:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        self.user = request.user
        self.product_id = request.POST.get('product_id')
        self.user_cart = Cart.objects.filter(user_id=self.user)

    def add_to_cart(self):
        product = get_object_or_404(Product, id=self.product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=self.user, product=product
        )
        if not created:
            print('NOT')
            cart_item.quantity += 1
            cart_item.save()

        print('OK')
        return JsonResponse({'success': True, 'quantity': cart_item.quantity})

    def delete_from_cart(self):
        cart_item = self.get_item_cart()
        cart_item.delete()
        new_amount = self.get_total_price()
        print(new_amount)

        return JsonResponse({'success': True, 'new_amount': new_amount})

    def add_item_cart(self):
        cart_item: Cart = self.get_item_cart()

        new_quantity = int(cart_item.quantity) + 1
        cart_item.quantity = new_quantity
        cart_item.save()
        new_amount = self.get_total_price()

        return JsonResponse({'success': True, 'quantity': new_quantity, 'new_amount': new_amount})

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

        new_amount = self.get_total_price()
        return JsonResponse({'success': True, 'quantity': quantity-1, 'last': last, 'new_amount': new_amount})


    def get_item_cart(self):
        return get_object_or_404(Cart, user_id=self.user, product_id=self.product_id)


    def get_total_price(self):
        return self.user_cart.aggregate(total_price=Sum(F('product__price') * F("quantity"))).get('total_price', 0)
