from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import AddGameForm, AddReviewForm
from .models import Product, Category, Review


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # product = Product.objects.filter(slug=self.kwargs[self.slug_url_kwarg])
        context['reviews'] = Review.posted.filter(product_id__slug=self.kwargs[self.slug_url_kwarg])
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])


class AddGame(PermissionRequiredMixin, CreateView):
    template_name = 'store/add_game.html'
    form_class = AddGameForm
    success_url = reverse_lazy('catalog')
    model = Product
    permission_required = 'store.add_product'


class UpdateGame(PermissionRequiredMixin, UpdateView):
    template_name = 'store/add_game.html'
    model = Product
    success_url = reverse_lazy('catalog')
    fields = '__all__'
    permission_required = 'store.edit_product'


class DeleteGame(PermissionRequiredMixin, DeleteView):
    template_name = 'store/add_game.html'
    model = Product
    success_url = reverse_lazy('catalog')
    permission_required = 'store.delete_product'


class AddReview(LoginRequiredMixin, CreateView):
    template_name = 'store/add_review.html'
    form_class = AddReviewForm
    success_url = reverse_lazy('catalog')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        slug = self.kwargs.get('slug')
        form.instance.product = get_object_or_404(Product, slug=slug)
        return super().form_valid(form)


class PendingReviews(PermissionRequiredMixin, ListView):
    template_name = 'store/pending_reviews.html'
    context_object_name = 'reviews'
    permission_required = 'store.edit_review'

    def get_queryset(self) -> QuerySet[Any]:
        return Review.pending.all()


def approve_review(request: HttpRequest):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        print(review_id)
        review: Review = Review.pending.get(pk=review_id)
        review.status = Review.Status.POSTED
        review.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def reject_review(request: HttpRequest):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review: Review = Review.pending.get(pk=review_id)
        review.delete()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
