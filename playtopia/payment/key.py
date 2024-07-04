import os

from django.conf import settings
from .models import Order, ActivationKey


class Key:
    def __init__(self, order) -> None:
        self.order: Order = order

    def create_text(self):
        text = f'Заказ {self.order.id}\n\n'
        for keys in self.get_keys():
            for game, key in keys.items():
                text += f'{game}: {key}\n'
        return text

    def get_keys(self):
        keys = []
        for item in self.order.items.all():
            game = item.product
            for _ in range(item.quantity):
                activation_key: ActivationKey = ActivationKey.issued.filter(game=game).first()
                activation_key.status = ActivationKey.Status.ISSUED
                activation_key.order_item = item
                activation_key.save()
                keys.append({game.name: activation_key.key})
        return keys

    def issue_activation_keys(self):
        text = self.create_text()

        keys_dir = os.path.join(settings.MEDIA_ROOT, 'keys')
        if not os.path.exists(keys_dir):
            os.makedirs(keys_dir)

        keys_file_path = os.path.join(keys_dir, f'order_{self.order.id}_keys.txt')

        with open(keys_file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        self.order.keys_file.name = f'keys/order_{self.order.id}_keys.txt'
        self.order.save()
