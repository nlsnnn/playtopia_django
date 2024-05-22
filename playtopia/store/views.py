from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

# Create your views here.
class MainPage(TemplateView):
    template_name = 'store/index.html'
