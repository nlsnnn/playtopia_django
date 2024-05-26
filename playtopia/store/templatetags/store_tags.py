from django import template
from django.db.models import Count

from store.models import Category

register = template.Library()

@register.inclusion_tag('store/list_categories.html')
def show_categories(cat_selected=1):
    cats = Category.objects.annotate(total=Count('products')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}
