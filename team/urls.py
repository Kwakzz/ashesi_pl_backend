from django.urls import path
from team.views import create_team, update_team, get_teams, get_mens_players_in_team, get_womens_players_in_team


urlpatterns = [
    path('team/create/', create_team, name='create_team'),
    path('team/update/<int:id>/', update_team, name='update_team'),
    path('team/get/', get_teams, name='get_teams'),
    path('team/mens_players/get', get_mens_players_in_team, name='get_mens_players_in_team'),
    path('team/womens_players/get', get_womens_players_in_team, name='get_womens_players_in_team'),
]