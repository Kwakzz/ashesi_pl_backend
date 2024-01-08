from django.urls import path
from player.views import create_player, update_player, get_players, get_player, create_coach, get_coaches, get_coach, update_coach, get_positions


urlpatterns = [
    path('player/create/', create_player, name='create_player'),
    path('player/update/<int:id>/', update_player, name='update_player'),
    path('player/get/', get_players, name='get_players'),
    path('player/get', get_player, name='get_player'),
    
    path('coach/create/', create_coach, name='create_coach'),
    path('coach/update/<int:id>/', update_coach, name='update_coach'),
    path('coach/get/', get_coaches, name='get_coaches'),
    path('coach/get', get_coach, name='get_coach'),
    
    path('position/get/', get_positions, name='get_positions'),
    
]