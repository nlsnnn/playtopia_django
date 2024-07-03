from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from django.urls import reverse, reverse_lazy

from .forms import (LoginUserForm, ProfileUserForm, RegisterUserForm,
                    UserPasswordChangeForm)
from .tasks import send_registration_mail
from payment.models import Order, OrderItem


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self) -> str:
        return reverse_lazy('catalog')


class LogoutUser(LogoutView):
    template_name = 'users/login.html'


class ProfileUser(UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset: QuerySet | None = ...) -> Model:
        return self.request.user


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        send_registration_mail.delay(form.instance.username,
                                     form.instance.email)
        return super().form_valid(form)

class PasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password-change-done')


class OrdersUser(ListView):
    template_name = 'users/orders.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet[reverse_lazy]:
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        for order in orders:
            order.products = [item.product for item in order.items.all()]
        return context


class ShowOrder(DetailView):
    template_name = 'users/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str]:
        context = super().get_context_data(**kwargs)
        order = context['order']
        order.products = [item.product for item in order.items.all()]
        print(order.products)
        return context

    def get_object(self, queryset: QuerySet[reverse_lazy] | None = ...) -> Model:
        return Order.objects.get(pk=self.kwargs['id'])
