from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView

from .models import Product


class MainPage(TemplateView):
    template_name = 'store/index.html'


class GamesList(ListView):
    template_name = 'store/catalog.html'
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.all()
