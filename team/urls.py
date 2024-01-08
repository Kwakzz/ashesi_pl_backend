from django.urls import path
from team.views import create_team, update_team, get_teams, get_team, get_mens_players_in_team, get_womens_players_in_team, get_team_stats, get_mens_team_stats, get_womens_team_stats


urlpatterns = [
    path('team/create/', create_team, name='create_team'),
    path('team/update/<int:id>/', update_team, name='update_team'),
    path('team/get/', get_teams, name='get_teams'),
    path('team/get', get_team, name='get_team'),
    path('team/mens_players/get', get_mens_players_in_team, name='get_mens_players_in_team'),
    path('team/womens_players/get', get_womens_players_in_team, name='get_womens_players_in_team'),
    path('team/stats/get', get_team_stats, name='get_team_stats'),
    path('team/mens_stats/get', get_mens_team_stats, name='get_mens_team_stats'),
    path('team/womens_stats/get', get_womens_team_stats, name='get_womens_team_stats'),
]