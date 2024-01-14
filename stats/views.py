from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from fixture.models import Goal, MatchEvent, Season, Match
from django.db.models import Q


@api_view(['GET'])
def get_mens_top_scorers(request):
    """See get_season_top_scorers for documentation
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_top_scorers(season_id_param, 'M')


@api_view(['GET'])
def get_womens_top_scorers(request):
    """See get_season_top_scorers for documentation
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_top_scorers(season_id_param, 'W')


@api_view(['GET'])
def get_mens_season_top_assisters(request):
    """Get the men's top assisters of a season. 
    
    Args:
    A get request. The request must contain the season id.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of men's players ranked by assists. The message is either 'Top men's assisters retrieved successfully' or 'Top men's assisters retrieval failed'.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_top_assisters(season_id_param, 'M')
    
    
    
@api_view(['GET'])
def get_womens_season_top_assisters(request):
    """See get_season_top_assisters for documentation.
    
    Args:
    A get request. The request must contain the season id.
    
    Returns:
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_top_assisters(season_id_param, 'W') 


@api_view(['GET'])
def get_mens_season_red_card_rankings(request):
    """See get_season_card_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_card_rankings(season_id_param, 'M', 'Red Card')


@api_view(['GET'])
def get_mens_season_yellow_card_rankings(request):
    """See get_season_card_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_card_rankings(season_id_param, 'M', 'Yellow Card')

@api_view(['GET'])
def get_womens_season_red_card_rankings(request):
    """See get_season_card_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_card_rankings(season_id_param, 'W', 'Red Card')

@api_view(['GET'])
def get_womens_season_yellow_card_rankings(request):
    """See get_season_card_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_card_rankings(season_id_param, 'W', 'Yellow Card')     



@api_view(['GET'])
def get_mens_season_clean_sheet_rankings(request):
    """See get_season_clean_sheet_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    
    return get_season_clean_sheet_rankings('M', season_id_param)

@api_view(['GET'])
def get_womens_season_clean_sheet_rankings(request):
    """See get_season_clean_sheet_rankings for documentation.
    
    Args:
    A get request. The request must contain the season id.
    """
    
    season_id_param = request.query_params.get('season_id')
    
    return get_season_clean_sheet_rankings('W', season_id_param)


def get_season_top_scorers(season_id_arg, gender):
    """Get the top scorers of a season. This is a helper function. It is called by get_mens_season_top_scorers and get_womens_season_top_scorers.
    
    Args:
    season_id_arg: The season of the ranking.
    gender: Men or women's top scorer rankings?
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of men's players ranked by goals scored. The message indicates successful or failed retrieval of rankings.
    """
    
    season_id_param = season_id_arg
    
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
    

    goals = Goal.objects.filter(
        Q(match_event__match__match_day__season=season) &
        Q(match_event__player__gender=gender)
    )
    
    
    if not goals:
        return Response({'message': 'No goals scored in this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    scorers = []
    
    for goal in goals:
            scorer_data = {
                'first_name': goal.match_event.player.first_name,
                'last_name': goal.match_event.player.last_name,
                'position': goal.match_event.player.position.name,
                'team_name': goal.match_event.player.team.name,
                'team_name_abbreviation': goal.match_event.player.team.name_abbreviation,
                'team_logo_url': goal.match_event.player.team.logo_url.url,
                'team_color': goal.match_event.player.team.color,
                'player_id': goal.match_event.player.id,
                'no_of_goals': Goal.objects.filter(
                    Q(match_event__player=goal.match_event.player),
                    Q(match_event__match__match_day__season=season)
                ).count()
            }
            if goal.match_event.player.image is not None:
                scorer_data['player_image'] = goal.match_event.player.image.url
                
            if scorer_data not in scorers:
                scorers.append(scorer_data)
        
    scorers.sort(key=lambda x: x['no_of_goals'], reverse=True)
    
    if gender == 'M':
        return Response({'message': 'Men\'s top scorers retrieved successfully', 'data': scorers}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Women\'s top scorers retrieved successfully', 'data': scorers}, status=status.HTTP_200_OK)

    

def get_season_top_assisters(season_id_arg, gender):
    """Get the top assisters of a season. This is a helper function. It's used by get_mens_season_top_assisters and get_womens_season_top_assisters.
    
    Args:
    A get request. The request must contain the season id.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of women's players ranked by assists. The message indicates whether the top assisters were retrieved successfully or not.
    """
    
    season_id_param = season_id_arg
    
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
    
    
    goals = Goal.objects.filter(
        Q(match_event__match__match_day__season=season) &
        Q(match_event__player__gender=gender)
    )
    
    if not goals:
        return Response({'message': 'No goals scored in this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    assisters = []
    
    for goal in goals:
        if goal.assist_provider:
            assister_data = {
                'first_name': goal.assist_provider.first_name,
                'last_name': goal.assist_provider.last_name,
                'position': goal.assist_provider.position.name,
                'team_name': goal.assist_provider.team.name,
                'team_name_abbreviation': goal.assist_provider.team.name_abbreviation,
                'team_logo_url': goal.assist_provider.team.logo_url.url,
                'team_color': goal.assist_provider.team.color,
                'player_id': goal.assist_provider.id,
                'no_of_assists': Goal.objects.filter(
                    Q(assist_provider=goal.assist_provider),
                    Q(match_event__match__match_day__season=season)
                ).count()
            }
            
            if goal.assist_provider.image is not None:
                assister_data['player_image'] = goal.assist_provider.image.url
            if assister_data not in assisters:
                assisters.append(assister_data)
        
    assisters.sort(key=lambda x: x['no_of_assists'], reverse=True)
    
    if gender == 'M':
        return Response({'message': 'Top men\'s assisters retrieved successfully', 'data': assisters}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Top women\'s assisters retrieved successfully', 'data': assisters}, status=status.HTTP_200_OK) 


def get_season_clean_sheet_rankings(gender, season_id_arg):
    """This is a helper function. Get the clean sheet rankings of a season. A team has a clean sheet in the following situations:
    1. They're the home team and the away_team_score is 0
    2. They're the away team and the home_team_score is 0
    
    Args:
    gender: Men's or women's clean sheet rankings?
    season_id_arg: The season id.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of teams ranked by clean sheets. The message indicates whether the clean sheet rankings were retrieved successfully or not. 
    """
    
    season_id_param = season_id_arg
    
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
    
    clean_sheets = Match.objects.filter(
        Q(match_day__season=season) &
        (Q(home_team_score=0) | Q(away_team_score=0)) &
        Q(competition__gender=gender) & 
        Q(has_ended=True)
    )
    
    if not clean_sheets:
        return Response({'message': 'No clean sheets this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    clean_sheet_rankings = []
    
    
    for clean_sheet in clean_sheets:
        if clean_sheet.home_team_score == 0:
            clean_sheet_ranking_data = {
                'team_name': clean_sheet.away_team.name,
                'team_name_abbreviation': clean_sheet.away_team.name_abbreviation,
                'team_logo_url': clean_sheet.away_team.logo_url.url,
                'team_color': clean_sheet.away_team.color,
                'no_of_clean_sheets': Match.objects.filter(
                    Q(away_team=clean_sheet.away_team) &
                    Q(home_team_score=0) &
                    Q(match_day__season=season) &
                    Q(competition__gender = gender) &
                    Q(has_ended=True)
                ).count()
            }
            if clean_sheet_ranking_data not in clean_sheet_rankings:
                clean_sheet_rankings.append(clean_sheet_ranking_data)
                
        if clean_sheet.away_team_score == 0:
            clean_sheet_ranking_data = {
                'team_name': clean_sheet.home_team.name,
                'team_name_abbreviation': clean_sheet.home_team.name_abbreviation,
                'team_logo_url': clean_sheet.home_team.logo_url.url,
                'team_color': clean_sheet.home_team.color,
                'no_of_clean_sheets': Match.objects.filter(
                    Q(home_team=clean_sheet.home_team) &
                    Q(away_team_score=0) &
                    Q(match_day__season=season) &
                    Q(competition__gender = gender) &
                    Q(has_ended=True)
                ).count()
            }
            if clean_sheet_ranking_data not in clean_sheet_rankings:
                clean_sheet_rankings.append(clean_sheet_ranking_data)
                
    clean_sheet_rankings.sort(key=lambda x: x['no_of_clean_sheets'], reverse=True)
    
    return Response({'message': 'Clean sheet rankings retrieved successfully', 'data': clean_sheet_rankings}, status=status.HTTP_200_OK)


def get_season_card_rankings(season_id_arg, gender, card_type):
    """This is a helper function Get the card rankings of a season. 
    
    Args:
    season_id_arg: The season id.
    gender: Men's or women's card rankings?
    card_type: Red or yellow card rankings?
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message, a list of errors if any, and a list of players ranked by cards. The message could be this: "<Card type> rankings retrieved successfully" or "No <Card type> this season yet".
    """
    
    season_id_param = season_id_arg
    
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
    
    cards = MatchEvent.objects.filter(
        Q(match__match_day__season=season) &
        Q(event_type=card_type) &
        Q(player__gender=gender)
    )
    
    if not cards:
        return Response({'message': 'No ' + card_type + ' cards this season yet'}, status=status.HTTP_404_NOT_FOUND)
    
    card_rankings = []
    
    for card in cards:
        card_ranking_data = {
            'first_name': card.player.first_name,
            'last_name': card.player.last_name,
            'position': card.player.position.name,
            'team_name': card.player.team.name,
            'team_name_abbreviation': card.player.team.name_abbreviation,
            'team_logo_url': card.player.team.logo_url.url,
            'team_color': card.player.team.color,
            'player_id': card.player.id,
            'no_of_cards': MatchEvent.objects.filter(
                Q(player=card.player) &
                Q(match__match_day__season=season) &
                Q(event_type=card_type)
            ).count()
        }
        if card.player.image is not None:
            card_ranking_data['player_image'] = card.player.image.url
        if card_ranking_data not in card_rankings:
            card_rankings.append(card_ranking_data)
        
    card_rankings.sort(key=lambda x: x['no_of_cards'], reverse=True)
    
    return Response({'message': card_type + ' rankings retrieved successfully', 'data': card_rankings}, status=status.HTTP_200_OK)