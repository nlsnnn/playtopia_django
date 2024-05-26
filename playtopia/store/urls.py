from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('catalog/', views.GamesList.as_view(), name='catalog'),
    path('category/<slug:category_slug>', views.GamesList.as_view(), name='category'),
    path('game/<slug:game_slug>', views.ShowGame.as_view(), name='game'),
]
