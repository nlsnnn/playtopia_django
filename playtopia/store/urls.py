from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view(), name='home'),
    path('catalog/', views.GamesList.as_view(), name='catalog'),
    path('catalog/<slug:category_slug>', views.CategoryGamesList.as_view(), name='category'),
    path('game/<slug:game_slug>', views.ShowGame.as_view(), name='game'),
    path('add-game/', views.AddGame.as_view(), name='add_game'),
    path('edit/<slug:slug>', views.UpdateGame.as_view(), name='edit'),
    path('delete/<slug:slug>', views.DeleteGame.as_view(), name='delete'),
    path('add-review/<slug:slug>', views.AddReview.as_view(), name='add_review'),
    path('pending-reviews/', views.PendingReviews.as_view(), name='pending_reviews'),
    path('approve-review/', views.approve_review, name='approve_review'),
    path('reject-review/', views.reject_review, name='reject_review')
]
