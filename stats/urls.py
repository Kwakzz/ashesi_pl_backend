from django.urls import path
from stats.views import get_season_top_scorers, get_season_top_assisters


urlpatterns = [
    path('season/stats/top_scorers/get', get_season_top_scorers, name='get_season_top_scorers'),
    path('season/stats/top_assisters/get', get_season_top_assisters, name='get_season_top_assisters'),
]