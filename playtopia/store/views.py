from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView

from .models import Product, Category


class MainPage(TemplateView):
    template_name = 'store/index.html'


class GamesList(ListView):
    template_name = 'store/catalog.html'
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.all()


class CategoryGamesList(ListView):
    template_name = 'store/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cat = context['products'][0].category
        context['cat_selected'] = cat.pk
        context['title'] = cat.name
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.filter(category__slug=self.kwargs['category_slug']).select_related('category')


class ShowGame(DetailView):
    model = Product
    template_name = 'store/game.html'
    slug_url_kwarg = 'game_slug'
    context_object_name = 'game'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])
