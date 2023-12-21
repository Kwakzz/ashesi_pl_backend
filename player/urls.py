from django.urls import path
from player.views import create_player, update_player, get_players, get_player


urlpatterns = [
    path('player/create/', create_player, name='create_player'),
    path('player/update/<int:id>/', update_player, name='update_player'),
    path('player/get/', get_players, name='get_players'),
    path('player/get', get_player, name='get_player'),
]