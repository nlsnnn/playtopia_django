from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Review, ActivationKey


admin.site.site_header = 'Админ панель'
admin.site.index_title = 'Playtopia'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['time_create', 'time_update']
    list_display = ['name', 'game_image', 'price', 'category', ]


    @admin.display(description='Фото')
    def game_image(self, product: Product):
        if product.photo:
            return mark_safe(f"<img src='{product.photo.url}' width=50>")
        return 'Без фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    list_display = ['id', 'name']


admin.site.register(Review)
admin.site.register(ActivationKey)
