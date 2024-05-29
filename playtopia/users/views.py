from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm


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
    slug_url_kwarg = 'user_slug'
    success_url = reverse_lazy('catalog')

    def get_object(self, queryset: QuerySet[reverse_lazy] | None = ...) -> Model:
        return self.request.user


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:login')
