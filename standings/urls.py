from django.urls import path
from standings.views import create_mens_league_table, create_womens_league_table, create_fa_cup_mens_group_standings, get_season_mens_league_standings, get_season_womens_league_standings, get_season_mens_fa_cup_group_standings, get_latest_mens_standings, get_season_standings, update_mens_league_standings

urlpatterns = [
    path('standings/league/mens/create/', create_mens_league_table, name='create_mens_league_table'),
    path('standings/league/womens/create/', create_womens_league_table, name='create_womens_league_table'),
    path('standings/fa_cup/group/mens/create/', create_fa_cup_mens_group_standings, name='create_fa_cup_mens_group_standings'),
    
    path('standings/season/get', get_season_standings, name='get_season_standings'),
    path('standings/league/mens/get', get_season_mens_league_standings, name='get_season_mens_league_standings'),
    path('standings/league/womens/get', get_season_womens_league_standings, name='get_season_womens_league_standings'),
    path('standings/fa_cup/group/mens/get', get_season_mens_fa_cup_group_standings, name='get_season_mens_fa_cup_group_standings'),
    path('standings/mens/latest/get/', get_latest_mens_standings, name='get_latest_mens_standings'),
    
    path('standings/league/mens/update/<int:season_id>/', update_mens_league_standings, name='update_mens_league_standings'),
    
]