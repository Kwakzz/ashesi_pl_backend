from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from player.models import Player
from player.serializers import PlayerSerializer
from team.models import Team
from team.serializers import TeamSerializer
from django.db.models import Q, F, Sum
from fixture.models import Competition, MatchEvent, Season, Match, Goal, Stage




@api_view(['POST'])
def create_team(request):
    
    """Create a new team. Its argument is a JSON request which is deserialized into a django model.
    
    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the team.
    name_abbreviation: The abbreviated name of the team.
    logo_url: The url of the team's logo.
    color: The color of the team.
    twitter_url: The url of the team's twitter page.
    

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Team created successfully' or 'Team creation failed'.
    """
    
    serializer = TeamSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Team created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Team creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PATCH'])
def update_team(request, id):
    """Update a team. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    name: The name of the team.
    name_abbreviation: The abbreviated name of the team.
    logo_url: The url of the team's logo.
    color: The color of the team.
    twitter_url: The url of the team's twitter page.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Team updated successfully' or 'Team update failed'.
    """
    
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Team updated successfully'}, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
def get_teams(request):
    """Get all teams.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of teams.
    """
        
    womens_teams = Team.objects.filter(
        Q(players__gender='W') & ~Q(players=None)
    ).distinct()
    
    teams = []
    
    for team in Team.objects.all():
        team = {
            'id': team.id,
            'name': team.name,
            'name_abbreviation': team.name_abbreviation,
            'logo_url': team.logo_url.url if team.logo_url else '',  # Extract URL from CloudinaryResource
            'cover_photo_url': team.cover_photo_url.url if team.cover_photo_url else '',  # Extract URL from CloudinaryResource
            'color': team.color,
            'twitter_url': team.twitter_url,
            'has_womens_team': team in womens_teams,
        }
        
        teams.append(team)
    
    return Response({'message': 'Teams retrieved successfully', 'data': teams}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_team(request):
    """Get a team.

    Args:
    request: A get request. The request must contain the id of the team to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the team.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team)
    return Response({'message': 'Team retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_mens_players_in_team(request):
    """Get all men's players in a team.

    Args:
    request: A get request. The request must contain the id of the team whose players are to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of men's players in a team.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    players = Player.objects.filter(team=team, gender='M')
    serializer = PlayerSerializer(players, many=True)
    
    if not serializer.data:
        return Response({'message': 'No men\'s player in' + team.name}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Men\'s players in ' + team.name + ' retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_womens_players_in_team(request):
    """Get all wommen's players in a team.

    Args:
    request: A get request. The request must contain the id of the team whose players are to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of women's players in a team.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    players = Player.objects.filter(team=team, gender='W')
    serializer = PlayerSerializer(players, many=True)
    
    if not serializer.data:
        return Response({'message': 'No women\'s player in' + team.name}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Women\'s players in ' + team.name + ' retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_mens_team_stats(request):
    """Get a men's team's stats.

    Args:
    request: A get request. The request must contain the id of the team whose stats are to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the team's stats.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    team_stats = {
        'wins': get_team_no_of_wins_by_gender(id, 'M'),
        'losses': get_team_no_of_losses_by_gender(id, 'M'),
        'draws': get_no_of_matches_played_by_gender(id, 'M') - get_team_no_of_wins_by_gender(id, 'M') - get_team_no_of_losses_by_gender(id, 'M'),
        'goals_scored': get_team_no_of_goals_scored_by_gender(id, 'M'),
        'goals_conceded': get_team_no_of_goals_conceded_by_gender(id, 'M'),
        'matches_played': get_no_of_matches_played_by_gender(id, 'M'),
    }

    return Response({'message': 'Men\'s team stats retrieved successfully', 'data': team_stats}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_womens_team_stats(request):
    """Get a women's team's stats.

    Args:
    request: A get request. The request must contain the id of the team whose stats are to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the team's stats.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    team_stats = {
        'wins': get_team_no_of_wins_by_gender(id, 'W'),
        'losses': get_team_no_of_losses_by_gender(id, 'W'),
        'draws': get_no_of_matches_played_by_gender(id, 'W') - get_team_no_of_wins_by_gender(id, 'W') - get_team_no_of_losses_by_gender(id, 'W'),
        'goals_scored': get_team_no_of_goals_scored_by_gender(id, 'W'),
        'goals_conceded': get_team_no_of_goals_conceded_by_gender(id, 'W'),
        'matches_played': get_no_of_matches_played_by_gender(id, 'W'),
    }

    return Response({'message': 'Women\'s team stats retrieved successfully', 'data': team_stats}, status=status.HTTP_200_OK)
    



@api_view(['GET'])
def get_team_stats(request):
    """Get a team's stats.

    Args:
    request: A get request. The request must contain the id of the team whose stats are to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the team's stats.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    team_stats = {
        'wins': get_team_no_of_wins(id),
        'losses': get_team_no_of_losses(id),
        'draws': get_no_of_matches_played(id) - get_team_no_of_wins(id) - get_team_no_of_losses(id),
        'goals_scored': get_team_no_of_goals_scored(id),
        'goals_conceded': get_team_no_of_goals_conceded(id),
        'matches_played': get_no_of_matches_played(id),
    }

    return Response({'message': 'Team stats retrieved successfully', 'data': team_stats}, status=status.HTTP_200_OK)





# HELPER FUNCTIONS

def get_team_no_of_wins(team_id):
    """Get the number of matches won by a team.

    Args:
        team_id: The id of the team whose number of matches won is to be retrieved.

    Returns:
        The number of matches won by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_won = Match.objects.filter(
        Q(home_team=team, home_team_score__gt=F('away_team_score')) |
        Q(away_team=team, away_team_score__gt=F('home_team_score'))
    ).count()

    return matches_won


def get_team_no_of_losses(team_id):
    """Get the number of matches lost by a team.

    Args:
        team_id: The id of the team whose number of matches lost is to be retrieved.

    Returns:
        The number of matches lost by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_lost = Match.objects.filter(
        Q(home_team=team, home_team_score__lt=F('away_team_score')) |
        Q(away_team=team, away_team_score__lt=F('home_team_score'))
    ).count()

    return matches_lost


def get_team_no_of_goals_scored(team_id):
    """Get the number of goals scored by a team.

    Args:
        team_id: The id of the team whose number of goals scored is to be retrieved.

    Returns:
        The number of goals scored by a team.
    """
    
    team = Team.objects.get(id=team_id)

    no_of_goals_scored = Goal.objects.filter(scoring_team=team).count()

    return no_of_goals_scored


def get_team_no_of_goals_conceded(team_id):
    """Get the number of goals conceded by a team.

    Args:
        team_id: The id of the team whose number of goals conceded is to be retrieved.

    Returns:
        The number of goals conceded by a team.
    """
    
    team = Team.objects.get(id=team_id)

    # Get the sum of away team score when the home team is the given team
    away_goals_conceded = Match.objects.filter(
        home_team=team,
    ).aggregate(Sum('away_team_score'))['away_team_score__sum'] or 0

    # Get the sum of home team score when the away team is the given team
    home_goals_conceded = Match.objects.filter(
        away_team=team,
    ).aggregate(Sum('home_team_score'))['home_team_score__sum'] or 0

    # Calculate the total goals conceded
    total_goals_conceded = away_goals_conceded + home_goals_conceded
    

    return total_goals_conceded or 0


def get_no_of_matches_played(team_id):
    """Get the number of matches played by a team.

    Args:
        team_id: The id of the team whose number of matches played is to be retrieved.

    Returns:
        The number of matches played by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_played = Match.objects.filter(
        Q(home_team=team) |
        Q(away_team=team)
    ).count()

    return matches_played


# BY GENDER

def get_team_no_of_wins_by_gender(team_id, gender):
    """Get the number of matches won by a team (by gender).

    Args:
        team_id: The id of the team whose number of matches lost is to be retrieved.
        gender: The gender of the team whose number of matches lost is to be retrieved.

    Returns:
        The number of matches won by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_won = Match.objects.filter(
        Q(home_team=team, home_team_score__gt=F('away_team_score'), competition__gender=gender) |
        Q(away_team=team, away_team_score__gt=F('home_team_score'), competition__gender=gender)
    ).count()

    return matches_won


def get_team_no_of_losses_by_gender(team_id, gender):
    """Get the number of matches lost by a team.

    Args:
        team_id: The id of the team whose number of matches lost is to be retrieved.
        gender: The gender of the team whose number of matches lost is to be retrieved.

    Returns:
        The number of matches lost by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_lost = Match.objects.filter(
        Q(home_team=team, home_team_score__lt=F('away_team_score'), competition__gender=gender) |
        Q(away_team=team, away_team_score__lt=F('home_team_score'), competition__gender=gender)
    ).count()

    return matches_lost


def get_team_no_of_goals_scored_by_gender(team_id, gender):
    """Get the number of goals scored by a team (by gender).

    Args:
        team_id: The id of the team whose number of goals scored is to be retrieved.
        gender: The gender of the team whose number of goals scored is to be retrieved.

    Returns:
        The number of goals scored by a team.
    """
    
    team = Team.objects.get(id=team_id)

    no_of_goals_scored = Goal.objects.filter(
        Q(scoring_team=team) &
        Q(match_event__match__competition__gender=gender)
    ).count()

    return no_of_goals_scored


def get_team_no_of_goals_conceded_by_gender(team_id, gender):
    """Get the number of goals conceded by a team.

    Args:
        team_id: The id of the team whose number of goals conceded is to be retrieved.
        gender: The gender of the team whose number of goals conceded is to be retrieved.

    Returns:
        The number of goals conceded by a team.
    """
    
    team = Team.objects.get(id=team_id)

    # Get the sum of away team score when the home team is the given team
    away_goals_conceded = Match.objects.filter(
        Q(home_team=team) &
        Q(competition__gender = gender)
    ).aggregate(Sum('away_team_score'))['away_team_score__sum'] or 0

    # Get the sum of home team score when the away team is the given team
    home_goals_conceded = Match.objects.filter(
        Q(away_team=team)&
        Q(competition__gender = gender)
    ).aggregate(Sum('home_team_score'))['home_team_score__sum'] or 0

    # Calculate the total goals conceded
    total_goals_conceded = away_goals_conceded + home_goals_conceded
    

    return total_goals_conceded or 0


def get_no_of_matches_played_by_gender(team_id, gender):
    """Get the number of matches played by a team (by gender).

    Args:
        team_id: The id of the team whose number of matches played is to be retrieved.
        gender: The gender of the team whose number of matches played is to be retrieved.

    Returns:
        The number of matches played by a team.
    """
    
    team = Team.objects.get(id=team_id)

    matches_played = Match.objects.filter(
        Q(home_team=team, competition__gender=gender) |
        Q(away_team=team, competition__gender=gender)
    ).count()

    return matches_played
