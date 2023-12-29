from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from fixture.models import Goal, Match, MatchDay, MatchEvent, Referee, Season

from fixture.serializers import GoalSerializer, MatchDaySerializer, MatchEventSerializer, MatchSerializer, RefereeSerializer, SeasonSerializer
from player.models import Player
from team.models import Team

# REFEREE VIEWS
@api_view(['POST'])
def create_referee(request):
    """Create a new referee. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the referee.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Referee created successfully' or 'Referee creation failed'.
    """
    
    serializer = RefereeSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Referee created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Referee creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_referees(request):
    """Retrieve all referees. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of referees and a message. The message is either 'Referees retrieved successfully' or 'No referees found'.
    """
    
    referees = Referee.objects.all()
    
    if referees:
        serializer = RefereeSerializer(referees, many=True)
        return Response({'data': serializer.data, 'message': 'Referees retrieved successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'message': 'No referees found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_referee(request):
    """Retrieve a referee. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a referee and a message. The message is either 'Referee retrieved successfully' or 'Referee not found'.
    """
    
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Referee ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Referee ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        referee = Referee.objects.get(id=id)
    except Referee.DoesNotExist:
        return Response({'message': 'Referee not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RefereeSerializer(referee)
    return Response({'message': 'Referee retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    
# SEASON VIEWS
@api_view(['POST'])
def create_season(request):
    """Create a new season. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the season.
    start_date: The start date of the season.
    end_date: The end date of the season.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Season created successfully' or 'Season creation failed'.
    """
    
    serializer = SeasonSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Season created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Season creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
  


@api_view(['GET'])
def get_seasons(request):
    """Retrieve all seasons. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of seasons and a message. The message is either 'Seasons retrieved successfully' or 'No seasons found'.
    """
    
    seasons = Season.objects.all()
    
    if seasons:
        serializer = SeasonSerializer(seasons, many=True)
        return Response({'data': serializer.data, 'message': 'Seasons retrieved successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'message': 'No seasons found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_season(request):
    """Retrieve a season. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a season and a message. The message is either 'Season retrieved successfully' or 'Season not found'.
    """
    
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SeasonSerializer(season)
    return Response({'message': 'Season retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_season(request, id):
    """Update a season. Its argument is a JSON request which is deserialized into a Django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    name: The name of the season.
    start_date: The start date of the season.
    end_date: The end date of the season.

    Returns:
    A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Season updated successfully' or 'Season update failed'.
    """
    try:
        season = Season.objects.get(id=id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SeasonSerializer(season, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Season updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Season update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# MATCH DAY VIEWS
@api_view(['POST'])
def create_match_day(request):
    """Create a new match day. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    number: The number of the match day.
    date: The date of the match day.
    season: The season of the match day.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Match day created successfully' or 'Match day creation failed'.
    """
    
    serializer = MatchDaySerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Match day created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Match day creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_match_days(request):
    """Retrieve all match days. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of match days and a message. The message is either 'Match days retrieved successfully' or 'No match days found'.
    """
    
    match_days = MatchDay.objects.all()
    
    if match_days:
        serializer = MatchDaySerializer(match_days, many=True)
        return Response({'match_days': serializer.data, 'message': 'Match days retrieved successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'message': 'No match days found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_match_day(request):
    """Retrieve a match day. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a match day and a message. The message is either 'Match day retrieved successfully' or 'Match day not found'.
    """
    
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Match day ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Match day ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_day = MatchDay.objects.get(id=id)
    except MatchDay.DoesNotExist:
        return Response({'message': 'Match day not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MatchDaySerializer(match_day)
    return Response({'message': 'Match day retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_match_day(request, id):
    """Update a match day. Its argument is a JSON request which is deserialized into a Django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    number: The number of the match day.
    date: The date of the match day.
    season: The season of the match day.

    Returns:
    A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Match day updated successfully' or 'Match day update failed'.
    """
    try:
        match_day = MatchDay.objects.get(id=id)
    except MatchDay.DoesNotExist:
        return Response({'message': 'Match day not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MatchDaySerializer(match_day, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Match day updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Match day update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
def get_season_match_days(request):
    """Retrieve all match days of a season along with the matches. Its argument is a GET request.

    Args:
    A GET request. The request must contain the following fields:
    season_id: The id of the season.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of match days with serialized matches and a message. The message is either 'Match days retrieved successfully' or 'No match days found'.
    """

    season_id = request.query_params.get('season_id')

    if not season_id:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season_id = int(season_id)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    match_days = MatchDay.objects.filter(season=season)
    match_day_serializer = MatchDaySerializer(match_days, many=True)
    # return Response({'season': SeasonSerializer(season).data, 'match_days': match_day_serializer.data, 'message': 'Match days retrieved successfully'}, status=status.HTTP_200_OK)
    return Response({'data': match_day_serializer.data, 'message': 'Match days retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_match_day_matches(request):
    """Retrieve all matches of a match day. Its argument is a GET request.

    Args:
    A GET request. The request must contain the following fields:
    match_day_id: The id of the match day.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of matches and a message. The message is either 'Matches retrieved successfully' or 'No matches found'.
    """

    match_day_id = request.query_params.get('match_day_id')

    if not match_day_id:
        return Response({'message': 'Match day ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_day_id = int(match_day_id)
    except ValueError:
        return Response({'message': 'Invalid Match day ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_day = MatchDay.objects.get(id=match_day_id)
    except MatchDay.DoesNotExist:
        return Response({'message': 'Match day not found'}, status=status.HTTP_404_NOT_FOUND)

    matches = Match.objects.filter(match_day=match_day)
    serializer = MatchSerializer(matches, many=True)
    # return Response({'match_day': MatchDaySerializer(match_day).data, 'matches': serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)
    return Response({'data': serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_season_fixtures(request):
    """Retrieve all fixtures (unplayed matches) of the current season. Its argument is a GET request.

    Args:
    A GET request. The request must contain the following fields:
    season_id: The id of the season.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of matches and a message. The message is either 'Matches retrieved successfully' or 'No matches found'.
    """

    latest_season = Season.objects.latest('id')
    season_id = latest_season.id

    if not season_id:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season_id = int(season_id)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    match_days = MatchDay.objects.filter(season=season)
    matches = Match.objects.filter(match_day__in=match_days, has_ended=False)
    match_serializer = MatchSerializer(matches, many=True)
    # return Response({'season': SeasonSerializer(season).data, 'matches': match_serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)
    return Response({'data': match_serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_latest_results(request):
    """Retrieve the latest results (played matches) of the current season. Its argument is a GET request. The latest results are the results of the latest match day.

    Args:
    A GET request. The request must contain the following fields:
    season_id: The id of the season.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of matches and a message. The message is either 'Matches retrieved successfully' or 'No matches found'.
    """

    latest_season = Season.objects.get(id=1)
    season_id = latest_season.id

    if not season_id:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season_id = int(season_id)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    match_days = MatchDay.objects.filter(season=season)
    matches = Match.objects.filter(match_day__in=match_days, has_ended=True).order_by('-match_day__date')
    match_serializer = MatchSerializer(matches, many=True)
    return Response({'data': match_serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_season_results(request):
    """Retrieve all results (played matches) of a season. Its argument is a GET request.

    Args:
    A GET request. The request must contain the following fields:
    season_id: The id of the season.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of matches and a message. The message is either 'Matches retrieved successfully' or 'No matches found'.
    """

    season_id = request.query_params.get('season_id')

    if not season_id:
        return Response({'message': 'Season ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season_id = int(season_id)
    except ValueError:
        return Response({'message': 'Invalid Season ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    match_days = MatchDay.objects.filter(season=season)
    matches = Match.objects.filter(match_day__in=match_days, has_ended=True)
    match_serializer = MatchSerializer(matches, many=True)
    # return Response({'season': SeasonSerializer(season).data, 'matches': match_serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)
    return Response({'data': match_serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)



# MATCH VIEWS
@api_view(['POST'])
def create_match(request):
    """Create a new match. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    home_team: The home team of the match.
    away_team: The away team of the match.
    match_day: The match day of the match.
    match_time: The time of the match.
    stage: The stage of the match.
    referee: The referee of the match.
    competition: The competition of the match.
    
    """
    
    serializer = MatchSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Match created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Match creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_matches(request):
    """Retrieve all matches. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of matches and a message. The message is either 'Matches retrieved successfully' or 'No matches found'.
    """
    
    matches = Match.objects.all()
    
    if matches:
        serializer = MatchSerializer(matches, many=True)
        return Response({'data': serializer.data, 'message': 'Matches retrieved successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'message': 'No matches found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_match(request):
    """Retrieve a match. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a match and a message. The message is either 'Match retrieved successfully' or 'Match not found'.
    """
    
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Match ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Match ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MatchSerializer(match)
    return Response({'message': 'Match retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update_match(request, id):
    """Update a match. Its argument is a JSON request which is deserialized into a Django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    home_team: The home team of the match.
    away_team: The away team of the match.
    match_day: The match day of the match.
    match_time: The time of the match.
    stage: The stage of the match.
    referee: The referee of the match.
    competition: The competition of the match.

    Returns:
    A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Match updated successfully' or 'Match update failed'.
    """
    try:
        match = Match.objects.get(id=id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MatchSerializer(match, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Match updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Match update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# MATCH EVENT VIEWS
@api_view(['POST'])
def create_goal(request):
    """Create a new goal. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    match: The match the goal was scored in.
    scoring_team: The scoring team of the goal.
    assist_provider: The assist provider of the goal. This field is optional.
    player: The player who scored the goal.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Goal created successfully' or 'Goal creation failed'.
    
    """
    
    data = request.data
    assist_provider = None
    
    # If assist provider is provided, set it to the value of the assist provider field. Also, ensure that the assist provider is not the same as the player.
    if data.get('assist_provider'):
        if data.get('assist_provider') == data.get('player'):
            return Response({'message': 'Player and assist provider cannot be the same'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            assist_provider = data.get('assist_provider')
            assist_provider = Player.objects.get(id=assist_provider)
            
    if not data.get('match') or not data.get('scoring_team') or not data.get('player') or not data.get('minute'):
        return Response({'message': 'Match, scoring team, player and minute are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    player = data.get('player')
    match = data.get('match')
    scoring_team = data.get('scoring_team')
    minute = data.get('minute')
    
    # obtain the match, player and scoring team objects
    match = Match.objects.get(id=match)
    player = Player.objects.get(id=player)
    scoring_team = Team.objects.get(id=scoring_team)
    
    if not match:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not player:
        return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not scoring_team:
        return Response({'message': 'Scoring team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not match.has_started:
        return Response({'message': 'Match has not started yet'}, status=status.HTTP_400_BAD_REQUEST)
    
    if match.has_ended:
        return Response({'message': 'Match has ended'}, status=status.HTTP_400_BAD_REQUEST)
    
    if player == assist_provider:
        return Response({'message': 'Player and assist provider cannot be the same'}, status=status.HTTP_400_BAD_REQUEST)
    
    if assist_provider and assist_provider.team != match.home_team and assist_provider.team != match.away_team:
        return Response({'message': 'Assist provider is not playing for the scoring team'}, status=status.HTTP_400_BAD_REQUEST)
    
    if player.team != match.home_team and player.team != match.away_team:
        return Response({'message': 'Player is not playing for the scoring team'}, status=status.HTTP_400_BAD_REQUEST)
    
    if player.gender != match.competition.gender:
        return Response({'message': 'Player is not playing in the competition'}, status=status.HTTP_400_BAD_REQUEST)
    
    if scoring_team != match.home_team and scoring_team != match.away_team:
        return Response({'message': 'Scoring team is not playing in the match'}, status=status.HTTP_400_BAD_REQUEST)
    
    match_event = MatchEvent.objects.create(match=match, player=player, minute=minute, event_type='Goal')
    
    goal = Goal.objects.create(match_event=match_event, scoring_team=scoring_team, assist_provider=assist_provider)
    
    # Update the match score
    if scoring_team.id == match.home_team.id:
        match.home_team_score += 1
    else:
        match.away_team_score += 1
        
    match.save()
    
    return Response({'message': 'Goal created successfully'}, status=status.HTTP_201_CREATED)
    
        
        
@api_view(['POST'])
def create_red_card_event(request):
    """Create a new red card event. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    match: The match the red card was issued in.
    player: The player who received the red card.
    minute: The minute the red card was issued in.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Red card event created successfully' or 'Red card event creation failed'.
    
    """
    
    return create_match_event(request, 'Red Card')


@api_view(['POST'])
def create_yellow_card_event(request):
    """Create a new yellow card event. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    match: The match the yellow card was issued in.
    player: The player who received the yellow card.
    minute: The minute the yellow card was issued in.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Yellow card event created successfully' or 'Yellow card event creation failed'.
    
    """
    
    return create_match_event(request, 'Yellow Card')


@api_view(['GET'])
def get_match_events_in_match(request):
    """Retrieve all match events. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of match events and a message. The message is either 'Match events retrieved successfully' or 'No match events found'.
    """
    
    match_id = request.query_params.get('match_id')

    if not match_id:
        return Response({'message': 'Match ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_id = int(match_id)
    except ValueError:
        return Response({'message': 'Invalid Match ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    match_events = MatchEvent.objects.filter(match=match)
    serializer = MatchEventSerializer(match_events, many=True)
    return Response({'data': serializer.data, 'message': 'Match events retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_team_match_events(request):
    
    match_id = request.query_params.get('match_id')
    team_id = request.query_params.get('team_id')
    
    if not match_id:
        return Response({'message': 'Match ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not team_id:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        match_id = int(match_id)
    except ValueError:
        return Response({'message': 'Invalid Match ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        team_id = int(team_id)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    match_events = MatchEvent.objects.filter(match=match, player__team=team)
    serializer = MatchEventSerializer(match_events, many=True)
    return Response({'data': serializer.data, 'message': 'Match events retrieved successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_goals_in_match(request):
    """Retrieve all goals in a match. Its argument is a GET request.

    Args:
    A GET request.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of goals and a message. The message is either 'Goals retrieved successfully' or 'No goals found'.
    """
    
    match_id = request.query_params.get('match_id')

    if not match_id:
        return Response({'message': 'Match ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_id = int(match_id)
    except ValueError:
        return Response({'message': 'Invalid Match ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    goals = Goal.objects.filter(match_event__match=match)
    serializer = GoalSerializer(goals, many=True)
    return Response({'data': serializer.data, 'message': 'Goals retrieved successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_goals_in_match_by_team(request):
    """Retrieve all goals in a match by a team. Its argument is a GET request.

    Args:
    A GET request. The request must contain the following fields:
    match_id: The id of the match.
    team_id: The id of the team.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of goals and a message. The message is either 'Goals retrieved successfully' or 'No goals found'.
    """

    match_id = request.query_params.get('match_id')
    team_id = request.query_params.get('team_id')

    if not match_id:
        return Response({'message': 'Match ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not team_id:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match_id = int(match_id)
    except ValueError:
        return Response({'message': 'Invalid Match ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team_id = int(team_id)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    goals = Goal.objects.filter(match_event__match=match, scoring_team=team)
    serializer = GoalSerializer(goals, many=True)
    return Response({'data': serializer.data, 'message': 'Goals retrieved successfully'}, status=status.HTTP_200_OK)



# HELPER FUNCTIONS
def create_match_event(request, event_type):
    """Create a new match event. Its argument is a JSON request which is deserialized into a django model. This is a generic function that is used by the create_red_card_event and create_yellow_card_event functions.
    
    Args:
    A JSON request. The request must contain the following fields:
    match: The match the event occurred in.
    player: The player who was involved in the event.
    minute: The minute the event occurred in.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either '<event_type> event created successfully' or '<event_type> event creation failed'.
    
    """
    
    data = request.data
    
    if not data.get('match') or not data.get('player') or not data.get('minute'):
        return Response({'message': 'Match, player and minute are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    player = data.get('player')
    match = data.get('match')
    minute = data.get('minute')
    
    # obtain the match and player objects
    match = Match.objects.get(id=match)
    player = Player.objects.get(id=player)
    
    if not match:
        return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not player:
        return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not match.has_started:
        return Response({'message': 'Match has not started yet'}, status=status.HTTP_400_BAD_REQUEST)
    
    if match.has_ended:
        return Response({'message': 'Match has ended'}, status=status.HTTP_400_BAD_REQUEST)
    
    if player.team != match.home_team and player.team != match.away_team:
        return Response({'message': 'Player is not playing in the match'}, status=status.HTTP_400_BAD_REQUEST)
    
    if player.gender != match.competition.gender:
        return Response({'message': 'Player is not playing in the competition'}, status=status.HTTP_400_BAD_REQUEST)
    
    match_event = MatchEvent.objects.create(match=match, player=player, minute=minute, event_type=event_type)
    
    return Response({'message': event_type + ' event created successfully'}, status=status.HTTP_201_CREATED)