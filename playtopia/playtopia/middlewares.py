from typing import Any
from social_core.exceptions import AuthCanceled
from django.shortcuts import redirect
from django.contrib import messages


class SocialAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, AuthCanceled):
            messages.error(request, "Авторизация отменена")
            return redirect('users:login')
        return None
