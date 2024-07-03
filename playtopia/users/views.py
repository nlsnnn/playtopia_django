from typing import Any
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import (LoginUserForm, ProfileUserForm, RegisterUserForm,
                    UserPasswordChangeForm)
from .tasks import send_registration_mail


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

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        send_registration_mail.delay(form.instance.username,
                                     form.instance.email)
        return super().form_valid(form)

class PasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password-change-done')
