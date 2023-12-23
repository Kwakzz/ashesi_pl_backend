from django.urls import path
from fixture.views import create_referee, create_season, get_seasons, update_season, get_referees, get_season, get_referee, create_match_day, get_match_days, get_match_day, update_match_day, get_match_day_matches, get_season_match_days, get_season_fixtures, get_season_results, create_match, get_matches, get_match, update_match, create_goal, create_yellow_card_event, create_red_card_event, get_match_events_in_match, get_goals_in_match


urlpatterns = [
    path('referee/create/', create_referee, name='create_referee'),
    path('referee/get/', get_referees, name='get_referees'),
    path('referee/get', get_referee, name='get_referee'),
    
    path('season/create/', create_season, name='create_season'),
    path('season/get/', get_seasons, name='get_seasons'),
    path('season/get', get_season, name='get_season'),
    path('season/update/<int:id>/', update_season, name='update_season'),
    path('season/match_days/get', get_season_match_days, name='get_season_match_days'),
    path('season/fixtures/get/', get_season_fixtures, name='get_season_fixtures'),
    path('season/results/get', get_season_results, name='get_season_results'),
    
    path('match_day/create/', create_match_day, name='create_match_day'),
    path('match_day/get/', get_match_days, name='get_match_days'),
    path('match_day/get', get_match_day, name='get_match_day'),
    path('match_day/update/<int:id>/', update_match_day, name='update_match_day'),
    path('match_day/matches/get', get_match_day_matches, name='get_match_day_matches'),
    
    path('match/create/', create_match, name='create_match'),
    path('match/get/', get_matches, name='get_matches'),
    path('match/get', get_match, name='get_match'),
    path ('match/update/<int:id>/', update_match, name='update_match'),
    
    path('match_event/goal/create/', create_goal, name='create_goal'),
    path('match_event/yellow_card/create/', create_yellow_card_event, name='create_yellow_card_event'),
    path('match_event/red_card/create/', create_red_card_event, name='create_red_card_event'),
    path('match_event/get', get_match_events_in_match, name='get_match_events_in_match'),
    path('goal/get', get_goals_in_match, name='get_goals_in_match'),
    
    
    
]