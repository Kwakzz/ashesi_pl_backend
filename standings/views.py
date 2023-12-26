from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from fixture.models import Competition, Season
from standings.models import Standings, StandingsTeam

from standings.serializers import StandingsSerializer
from team.models import Team

# Create your views here.
@api_view(['POST'])
def create_fa_cup_group_standings(request):
    """Create a new FA Cup group standings. Its argument is a JSON request which is deserialized into a django model. For now, only the men's FA Cup is supported. The women don't play group stages.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the FA Cup group standings. This is a foreign key to the Season model.
    group_name: The name of the group.
    team1: The first team in the group. This is a foreign key to the Team model.
    team2: The second team in the group. This is a foreign key to the Team model.
    team3: The third team in the group. This is a foreign key to the Team model.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'FA Cup group standings created successfully' or 'FA Cup group standings creation failed'.
    """
    
    data = request.data
    
    # get the season
    season = Season.objects.get(id=data['season'])
    
    # get the competition
    competition = Competition.objects.get(
        name='FA Cup',
        gender='M'
    )
    
    # get the teams
    team1 = Team.objects.get(id=data['team1'])
    team2 = Team.objects.get(id=data['team2'])
    team3 = Team.objects.get(id=data['team3'])
    
    # create the standings
    standings = Standings.objects.create(season=season, competition=competition, group_name=data['group_name'])
    
    # create the standings teams
    standings_team1 = StandingsTeam.objects.create(standings=standings, team=team1)
    standings_team2 = StandingsTeam.objects.create(standings=standings, team=team2)
    standings_team3 = StandingsTeam.objects.create(standings=standings, team=team3)
    
    return Response({'message': 'FA Cup group standings created successfully'}, status=status.HTTP_201_CREATED)


def create_league_table(season_id, gender):
    """Create a new league table. Its argument is a JSON request which is deserialized into a django model. Both men and women have league tables.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league table. This is a foreign key to the Season model.
   
   Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'League table created successfully' or 'League table creation failed'.
    """
       
    # get the season
    season = Season.objects.get(id=season_id)
    
    competition = Competition.objects.get(
        name = 'Premier League',
        gender = gender
    )
    
    # create standings
    standings = Standings.objects.create(season=season, competition=competition, name='League Table')
    
    # add teams to the standings
    