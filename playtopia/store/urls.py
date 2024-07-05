from django.views.decorators.cache import cache_page
from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('catalog/', cache_page(60)(views.GamesList.as_view()), name='catalog'),
    path('catalog/<slug:category_slug>', cache_page(60 )(views.CategoryGamesList.as_view()), name='category'),
    path('game/<slug:game_slug>', cache_page(60 * 10)(views.ShowGame.as_view()), name='game'),
    path('add-game/', cache_page(60 * 60)(views.AddGame.as_view()), name='add_game'),
    path('edit/<slug:slug>', views.UpdateGame.as_view(), name='edit'),
    path('delete/<slug:slug>', views.DeleteGame.as_view(), name='delete'),
    path('add-review/<slug:slug>', views.AddReview.as_view(), name='add_review'),
    path('pending-reviews/', views.PendingReviews.as_view(), name='pending_reviews'),
    path('approve-review/', views.approve_review, name='approve_review'),
    path('reject-review/', views.reject_review, name='reject_review')
]
