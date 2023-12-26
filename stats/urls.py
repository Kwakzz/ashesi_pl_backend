from django.urls import path
from stats.views import get_season_top_scorers, get_season_top_assisters, get_mens_top_scorers, get_womens_top_scorers, get_mens_season_top_assisters, get_womens_season_top_assisters, get_mens_season_red_card_rankings, get_mens_season_yellow_card_rankings, get_womens_season_red_card_rankings, get_womens_season_yellow_card_rankings, get_mens_season_clean_sheet_rankings, get_womens_season_clean_sheet_rankings


urlpatterns = [
    path('season/stats/top_scorers/get', get_season_top_scorers, name='get_season_top_scorers'),
    path('season/stats/top_assisters/get', get_season_top_assisters, name='get_season_top_assisters'),
    
    path('season/stats/mens_top_scorers/get', get_mens_top_scorers, name='get_mens_top_scorers'),
    path('season/stats/womens_top_scorers/get', get_womens_top_scorers, name='get_womens_top_scorers'),

    path('season/stats/mens_top_assisters/get', get_mens_season_top_assisters, name='get_mens_season_top_assisters'),
    path('season/stats/womens_top_assisters/get', get_womens_season_top_assisters, name='get_womens_season_top_assisters'),
    
    path('season/stats/mens_red_card_rankings/get', get_mens_season_red_card_rankings, name='get_mens_season_red_card_rankings'),
    path('season/stats/mens_yellow_card_rankings/get', get_mens_season_yellow_card_rankings, name='get_mens_season_yellow_card_rankings'),
    path('season/stats/womens_red_card_rankings/get', get_womens_season_red_card_rankings, name='get_womens_season_red_card_rankings'),
    path('season/stats/womens_yellow_card_rankings/get', get_womens_season_yellow_card_rankings, name='get_womens_season_yellow_card_rankings'),
    
    path('season/stats/mens_clean_sheet_rankings/get', get_mens_season_clean_sheet_rankings, name='get_mens_season_clean_sheet_rankings'),
    path('season/stats/womens_clean_sheet_rankings/get', get_womens_season_clean_sheet_rankings, name='get_womens_season_clean_sheet_rankings'),
    
    
]