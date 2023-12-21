from django.urls import path
from team.views import create_team, update_team, get_teams


urlpatterns = [
    path('team/create/', create_team, name='create_team'),
    path('team/update/<int:id>/', update_team, name='update_team'),
    path('team/get/', get_teams, name='get_teams'),
]