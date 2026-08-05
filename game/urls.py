from django.urls import path
from . import views
from .views import SaveScoreView

urlpatterns = [
    path('', views.game_index, name='game_index'),
    path('api/save-score/', views.save_score, name='save_score'),
    path('api/save-score/', SaveScoreView.as_view(), name='save_score'),
]