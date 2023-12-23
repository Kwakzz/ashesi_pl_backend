from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from fixture.models import Goal, Season
from player.models import Player, PlayerPosition
from player.serializers import PlayerSerializer, PlayerPositionSerializer


@api_view(['GET'])
def get_season_top_scorers(request):
    """Get the top scorers of a season. 
    
    Args:
    A get request. The request must contain the season id.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of players ranked by goals scored. The message is either 'Top scorers retrieved successfully' or 'Top scorers retrieval failed'.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    if not season_id_param:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        season_id = int(season_id_param)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    goals = Goal.objects.filter(match_event__match__match_day__season=season)
    
    if not goals:
        return Response({'message': 'No goals scored in this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    scorers = []
    
    for goal in goals:
        scorer_data = {
            'first_name': goal.match_event.player.first_name,
            'last_name': goal.match_event.player.last_name,
            'position': goal.match_event.player.position.name,
            'team': goal.match_event.player.team.name,
            'team_logo': goal.match_event.player.team.logo_url,
            'player_id': goal.match_event.player.id,
            'player_image': goal.match_event.player.image,
            'no_of_goals': Goal.objects.filter(match_event__player=goal.match_event.player).count()
        }
        scorers.append(scorer_data)
        
    scorers.sort(key=lambda x: x['no_of_goals'], reverse=True)
    
    return Response({'message': 'Top scorers retrieved successfully', 'data': scorers}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_season_top_assisters(request):
    """Get the top assisters of a season. 
    
    Args:
    A get request. The request must contain the season id.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of players ranked by assists. The message is either 'Top assisters retrieved successfully' or 'Top assisters retrieval failed'.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    if not season_id_param:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        season_id = int(season_id_param)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    goals = Goal.objects.filter(match_event__match__match_day__season=season)
    
    if not goals:
        return Response({'message': 'No goals scored in this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    assisters = []
    
    for goal in goals:
        if goal.assist_provider:
            assister_data = {
                'first_name': goal.assist_provider.first_name,
                'last_name': goal.assist_provider.last_name,
                'position': goal.assist_provider.position.name,
                'team': goal.assist_provider.team.name,
                'team_logo': goal.assist_provider.team.logo_url,
                'player_id': goal.assist_provider.id,
                'player_image': goal.assist_provider.image,
                'no_of_assists': Goal.objects.filter(assist_provider=goal.assist_provider).count()
            }
            assisters.append(assister_data)
        
    assisters.sort(key=lambda x: x['no_of_assists'], reverse=True)
    
    return Response({'message': 'Top assisters retrieved successfully', 'data': assisters}, status=status.HTTP_200_OK)
    
    