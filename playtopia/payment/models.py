from django.db import models
from django.contrib.auth import get_user_model

from store.models import Product

class NotIssuedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=ActivationKey.Status.NOT_ISSUED)


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keys_file = models.FileField(upload_to='keys/', null=True, blank=True, verbose_name='Файл с ключами')

    def __str__(self) -> str:
        return f'Заказ {self.id}'

    class Meta:
        ordering = ['-created']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


class ActivationKey(models.Model):
    class Status(models.IntegerChoices):
        ISSUED = 1, 'Выдан'
        NOT_ISSUED = 0, 'Не выдан'

    key = models.CharField(max_length=20, unique=True, verbose_name='Ключ')
    game = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Игра')
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_ISSUED, verbose_name='Статус')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Товар')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    objects = models.Manager()
    issued = NotIssuedManager()

    def __str__(self) -> str:
        return self.key
