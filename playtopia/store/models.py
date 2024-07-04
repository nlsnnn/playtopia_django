from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='games/', default=None, blank=True,
                              null=True, verbose_name='Обложка')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(verbose_name='Статус')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Категории')

    def get_absolute_url(self):
        return reverse('game', kwargs={'game_slug': self.slug})

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class PendingManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Review.Status.PENDING)

class PostedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Review.Status.POSTED)


class Review(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, 'Не опубликован'
        POSTED = 1, 'Опубликован'

    class Meta:
        ordering = ['-time_create']

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    rating = models.IntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING, verbose_name='Статус')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    objects = models.Manager()
    pending = PendingManager()
    posted = PostedManager()

    def __str__(self) -> str:
        return self.text




class Cart(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Игра', related_name='cart_product')
    quantity = models.IntegerField(default=1)


class UploadFiles(models.Model):
    file = models.FileField(upload_to='playtopia/games')
