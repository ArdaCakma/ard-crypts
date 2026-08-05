from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_index, name='game_index'),
    path('api/save-score/', views.save_score, name='save_score'),
]