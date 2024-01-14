from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from fixture.models import Competition, MatchEvent, Season, Match, Goal, Stage
from standings.models import Standings, StandingsTeam
from standings.serializers import StandingsSerializer
from team.models import Team
from django.db.models import Q, F, Sum
import random



# Create your views here.
@api_view(['POST'])
def create_fa_cup_mens_group_standings(request):
    """This function creates the group standings for the FA Cup. The FA Cup is a knockout competition, but the group standings are used to determine the teams that progress to the knockout stages. The group standings are created by randomly assigning the six men's teams to two groups of three teams each. The group standings are created for a season.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the FA Cup group standings. This is a foreign key to the Season model.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'FA Cup group standings created successfully' or 'FA Cup group standings creation failed'.
    """
    
    data = request.data
    
    # get the season
    season = Season.objects.get(id=data.get('season'))
    
    if not season:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # get the men's FA Cup competition
    competition = Competition.objects.get(
        name='FA Cup',
        gender='M'
    )
    
    if not competition:
        return Response({'message': 'FA Cup not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # get all teams
    teams = Team.objects.all()
    
    if not teams:
        return Response({'message': 'No teams found'}, status=status.HTTP_404_NOT_FOUND)
    
    teams = list(teams)
    
    # shuffle the teams
    random.shuffle(teams)
    
    # create groups
    group_a = teams[:3]
    group_b = teams[3:6]
    
    # create standings
    
    try:
        standings_a = Standings.objects.create(season=season, competition=competition, name='A')
        standings_b = Standings.objects.create(season=season, competition=competition, name='B')
        
        for team in group_a:
            StandingsTeam.objects.create(standings=standings_a, team=team)
            
        for team in group_b:
            StandingsTeam.objects.create(standings=standings_b, team=team)
            
        return Response({'message': 'FA Cup group standings created successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'message': 'FA Cup group standings creation failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def create_league_table(season_id, gender, teams):
    """Create a new league table. Its argument is a JSON request which is deserialized into a django model. Both men and women have league tables.

    Args:
    season_id: The season of the league table. This is a foreign key to the Season model.
    gender: Men's or women's league table?
    teams: The teams in the league table. This is a list of foreign keys to the Team model. For men's league table creations, it's all men's teams, and for women, it's all women's teams.
   
   Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'League table created successfully' or 'League table creation failed'.
    """
       
    # get the season
    season = Season.objects.get(id=season_id)
    
    if not season:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
        
    try: 
        competition = Competition.objects.get(
            name = 'Premier League',
            gender = gender
        )
        
        # create standings
        standings = Standings.objects.create(season=season, competition=competition, name='League Table')
        
        for team in teams:
            StandingsTeam.objects.create(standings=standings, team=team)
            
        return Response({'message': 'League table created successfully'}, status=status.HTTP_201_CREATED)
    
    
    except Exception as e:
        return Response({'message': 'League table creation failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
        
@api_view(['POST']) 
def create_mens_league_table(request):
    """Create a men's league table for a season. See create_league_table for documentation.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league table. This is a foreign key to the Season model.
    """
    data = request.data
    season_id = data.get('season')
    
    mens_teams = Team.objects.filter(
        Q(players__gender='M') & ~Q(players=None)
    ).distinct()
    
    return create_league_table(season_id, 'M', mens_teams)


@api_view(['POST'])
def create_womens_league_table(request):
    """Create a women's league table for a season. See create_league_table for documentation.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league table. This is a foreign key to the Season model.
    """
    
    data = request.data
    season_id = data.get('season')
    
    womens_teams = Team.objects.filter(
        Q(players__gender='W') & ~Q(players=None)
    ).distinct()
    
    return create_league_table(season_id, 'W', womens_teams)


@api_view(['GET'])
def get_season_mens_fa_cup_group_standings(request):
    """Get the standings for the FA Cup group stage for a season.
    
    Args:
    A JSON request. The request must contain the following fields:
    
    season: The season of the FA Cup group standings. This is a foreign key to the Season model.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains the standings for the season and competition. The status code is either 200 or 404.
    """
    
    season_id = request.query_params.get('season_id')
    
    if not season_id:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        
        season = Season.objects.get(id=season_id)
        
        competition = Competition.objects.get(
            name='FA Cup',
            gender='M'
        )
        
        if not competition:
            return Response({'message': 'FA Cup not found'}, status=status.HTTP_404_NOT_FOUND)
        
        standings = Standings.objects.filter(
            season=season,
            competition=competition
        )
        
        if not standings:
            return Response({'message': 'FA Cup group standings not found'}, status=status.HTTP_404_NOT_FOUND)
        
        update_mens_fa_cup_standings(season_id)
        
        serializer = StandingsSerializer(standings, many=True)
        
        return Response({'data': serializer.data, 'message': 'FA Cup group standings retrieved'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'An error occurred', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
def get_season_standings(request):
    """Get the standings for a season.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the standings. This is a foreign key to the Season model.
    """
    
    
    season_id = request.query_params.get('season_id')
    
    if not season_id:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        standings = Standings.objects.filter(
            season_id=season_id
        )
        
        serializer = StandingsSerializer(standings, many=True)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Standings not found', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)


def get_league_standings(season_id, competition_id):
    """Get the standings for a season and competition. This is a helper function.

    Args:
    season_id: The season of the standings. This is a foreign key to the Season model.
    competition_id: The competition of the standings. This is a foreign key to the Competition model.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains the standings for the season and competition. The status code is either 200 or 404.
    """
    
    try:
        standings = Standings.objects.get(
            season_id=season_id,
            competition_id=competition_id
        )
        
        serializer = StandingsSerializer(standings)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Standings not found', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def get_season_mens_league_standings(request):
    """See get_standings for documentation.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league standings. This is a foreign key to the Season model.
    """
        
    season_id = request.query_params.get('season_id')
    
    league = Competition.objects.get(
        name = 'Premier League',
        gender = 'M'
    )
    
    update_league_standings(season_id, 'M')
        
    return get_league_standings(season_id, league.id)


@api_view(['GET'])
def get_season_womens_league_standings(request):
    """See get_standings for documentation.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league standings. This is a foreign key to the Season model.
    """
        
    season_id = request.query_params.get('season_id')
    
    league = Competition.objects.get(
        name = 'Premier League',
        gender = 'W'
    )
    
    update_league_standings(season_id, 'W')
        
    return get_league_standings(season_id, league.id) 

@api_view(['GET'])
def get_season_standings(request):
    """Get the standings for a season.

    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the standings. This is a foreign key to the Season model.
    """
    
    
    season_id = request.query_params.get('season_id')
    
    if not season_id:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        standings = Standings.objects.filter(
            season_id=season_id
        )
        
        serializer = StandingsSerializer(standings, many=True)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Standings not found', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)



def get_team_no_of_wins_in_league_campaign(season_id, team_id, gender):
    
    """Get the number of wins for a team in a league campaign. This is a helper function. It finds the number of matches where the team was the home team and the home team score was greater than the away team score, and the number of matches where the team was the away team and the away team score was greater than the home team score.
    
    Args:
    season_id: The season of the league campaign. This is a foreign key to the Season model.
    team_id: The team in the league campaign. This is a foreign key to the Team model.
    gender: Men's or women's league campaign?

    Returns:
        The number of wins for the team in the league campaign.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    competition = Competition.objects.get(
        name = "Premier League",
        gender = gender
    )

    matches_won = Match.objects.filter(
        Q(home_team=team, home_team_score__gt=F('away_team_score'), competition=competition, match_day__season=season) |
        Q(away_team=team, away_team_score__gt=F('home_team_score'), competition=competition, match_day__season=season)
    ).count()

    return matches_won


def get_team_no_of_losses_in_league_campaign(season_id, team_id, gender):
    
    """Get the number of losses for a team in a league campaign. This is a helper function. It finds the number of matches where the team was the home team and the home team score was less than the away team score, and the number of matches where the team was the away team and the away team score was less than the home team score.
    
    Args:
    season_id: The season of the league campaign. This is a foreign key to the Season model.
    team_id: The team in the league campaign. This is a foreign key to the Team model.
    gender: Men's or women's league campaign?

    Returns:
        The number of losses for the team in the league campaign.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    competition = Competition.objects.get(
        name = "Premier League",
        gender = gender
    )

    matches_lost = Match.objects.filter(
        Q(home_team=team, home_team_score__lt=F('away_team_score'), competition=competition, match_day__season=season) |
        Q(away_team=team, away_team_score__lt=F('home_team_score'), competition=competition, match_day__season=season)
    ).count()

    return matches_lost


def get_team_no_of_goals_scored_in_league_campaign_(season_id, team_id, gender):
    
    """Get the number of goals scored by a team in a league campaign. This is a helper function. It finds the number of goals where the scoring team was the team and the match was in the league campaign.
    
    Args:
    season_id: The season of the league campaign. This is a foreign key to the Season model.
    team_id: The team in the league campaign. This is a foreign key to the Team model.
    gender: Men's or women's league campaign?

    Returns:
        The number of goals scored by the team in the league campaign.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    competition = Competition.objects.get(
        name = "Premier League",
        gender = gender
    )

    no_of_goals_scored = Goal.objects.filter(
            Q(match_event__team=team) &
            Q(match_event__match__competition = competition, match_event__match__match_day__season=season)
        ).count()

    return no_of_goals_scored

def get_team_no_of_goals_conceded_in_league_campaign(season_id, team_id, gender):
    """Get the number of goals conceded by a team in a league campaign. This is a helper function. It finds sum of the away team score when the home team was the team in question and the match was in the league campaign, and the sum of the home team score when the away team was the team in question and the match was in the league campaign.

    Args:
        season_id: The season of the league campaign. This is a foreign key to the Season model.
        team_id: The team in the league campaign. This is a foreign key to the Team model.
        gender: Men's or women's league campaign?

    Returns:
        The number of goals conceded by the team in the league campaign.
    """
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    competition = Competition.objects.get(
        name = "Premier League",
        gender = gender
    )

    # Get the sum of away team score when the home team is the given team
    away_goals_conceded = Match.objects.filter(
        home_team=team,
        competition = competition,
        match_day__season=season
    ).aggregate(Sum('away_team_score'))['away_team_score__sum'] or 0

    # Get the sum of home team score when the away team is the given team
    home_goals_conceded = Match.objects.filter(
        away_team=team,
        competition = competition,
        match_day__season=season
    ).aggregate(Sum('home_team_score'))['home_team_score__sum'] or 0

    # Calculate the total goals conceded
    total_goals_conceded = away_goals_conceded + home_goals_conceded
    

    return total_goals_conceded or 0

def get_team_no_of_league_matches_played(season_id, team_id, gender):
    
    """Get the number of matches played by a team in a league campaign.
    
    Args:
        season_id: The season of the league campaign. This is a foreign key to the Season model.
        team_id: The team in the league campaign. This is a foreign key to the Team model.
        gender: Men's or women's league campaign?

    Returns:
        The number of matches played by team in a league campaign.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    competition = Competition.objects.get(
        name = "Premier League",
        gender = gender
    )

    no_of_league_matches_played = Match.objects.filter(
        Q(match_day__season=season, competition=competition, home_team=team, has_started=True) |
        Q(match_day__season=season, competition=competition, away_team=team, has_started=True)
    ).count()
        

    return no_of_league_matches_played 


def update_league_standings(season_id_arg, gender):
    
    """Update the standings for a league campaign. This is a helper function. It finds the standings for the league campaign, and updates the matches won, matches lost, goals for, goals against, and matches played for each team in the standings.
    These values are used to calculate other values like goal difference and matches drawn.
    
    Args:
    season_id_arg: The season of the league standings. This is a foreign key to the Season model.
    gender: Men's or women's league standings?
     
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Standings updated successfully' or 'Standings update failed'.
    """   
    try: 
        season_id = season_id_arg
        
        season = Season.objects.get(id=season_id)
        
        if not season:
            return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
        standings = Standings.objects.get(
            season = season,
            competition__name = 'Premier League',
            competition__gender = gender
        )
        
        if not standings:
            return Response({'message': 'Standings not found. Perhaps there was no Premier League competition during this season'}, status=status.HTTP_404_NOT_FOUND)
        
        standings_teams = StandingsTeam.objects.filter(standings=standings)
        
        for standings_team in standings_teams:
            team = standings_team.team
            standings_team.matches_won = get_team_no_of_wins_in_league_campaign(season_id, team.id, gender)
            standings_team.matches_lost = get_team_no_of_losses_in_league_campaign(season_id, team.id, gender)
            standings_team.goals_for = get_team_no_of_goals_scored_in_league_campaign_(season_id, team.id, gender)
            standings_team.goals_against = get_team_no_of_goals_conceded_in_league_campaign(season_id, team.id, gender)
            standings_team.matches_played = get_team_no_of_league_matches_played(season_id, team.id, gender)
            standings_team.save()
            
        return Response({'message': 'Standings updated successfully'}, status=status.HTTP_200_OK)
    
    except Standings.DoesNotExist:
        return Response({'message': 'Standings not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'message': 'Standings update failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    


def get_team_no_of_wins_in_fa_cup_group_stage(season_id, team_id, gender):
    
    """Get the number of wins for a team in an FA Cup competition's group stage. This is a helper function. It finds the number of matches where the team was the home team and the home team score was greater than the away team score, and the number of matches where the team was the away team and the away team score was greater than the home team score.
    
    Args:
    season_id: The season of the FA Cup competition. This is a foreign key to the Season model.
    team_id: The team in the FA Cup competition. This is a foreign key to the Team model.
    gender: Men's or women's FA Cup competition?

    Returns:
        The number of wins for the team in the FA Cup group stage during a particular season.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    stage = Stage.objects.get(name="Group Stage")
    competition = Competition.objects.get(
        name = "FA Cup",
        gender = gender
    )

    matches_won = Match.objects.filter(
        Q(home_team=team, home_team_score__gt=F('away_team_score'), competition=competition, match_day__season=season, stage=stage) |
        Q(away_team=team, away_team_score__gt=F('home_team_score'), competition=competition, match_day__season=season, stage = stage)
    ).count()

    return matches_won


def get_team_no_of_losses_in_fa_cup_group_stage(season_id, team_id, gender):
    
    """Get the number of losses for a team in an FA Cup's group stage. This is a helper function. It finds the number of matches where the team was the home team and the home team score was less than the away team score, and the number of matches where the team was the away team and the away team score was less than the home team score.
    
    Args:
    season_id: The season of the FA Cup competition. This is a foreign key to the Season model.
    team_id: The team in the FA Cup competition. This is a foreign key to the Team model.
    gender: Men's or women's FA Cup competition?


    Returns:
        The number of losses for the team in the the FA Cup group stage during a particular season.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    stage = Stage.objects.get(name="Group Stage")
    competition = Competition.objects.get(
        name = "FA Cup",
        gender = gender
    )

    matches_lost = Match.objects.filter(
        Q(home_team=team, home_team_score__lt=F('away_team_score'), competition=competition, match_day__season=season, stage=stage) |
        Q(away_team=team, away_team_score__lt=F('home_team_score'), competition=competition, match_day__season=season, stage=stage)
    ).count()

    return matches_lost


def get_team_no_of_goals_scored_in_fa_cup_group_stage(season_id, team_id, gender):
    
    """Get the number of goals scored by a team in an FA Cup's group stage. This is a helper function. It finds the number of goals where the scoring team was the team and the match was in the the FA Cup's group stage.
    
    Args:
    season_id: The season of the FA Cup competition. This is a foreign key to the Season model.
    team_id: The team in the FA Cup competition. This is a foreign key to the Team model.
    gender: Men's or women's FA Cup competition?

    Returns:
        The number of goals scored by the team in the FA Cup group stage during a particular season..
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    stage = Stage.objects.get(name="Group Stage")
    competition = Competition.objects.get(
        name = "FA Cup",
        gender = gender
    )

    no_of_goals_scored = Goal.objects.filter(
            Q(match_event__team=team) &
            Q(match_event__match__competition__name="FA Cup", match_event__match__competition=competition, match_event__match__match_day__season=season, match_event__match__stage=stage)
        ).count()

    return no_of_goals_scored


def get_team_no_of_goals_conceded_in_fa_cup_group_stage(season_id, team_id, gender):
    """Get the number of goals conceded by a team in an FA Cup's group stage. This is a helper function. It finds sum of the away team score where the home team was the team and the match was in the FA Cup's group stage, and the sum of the home team score where the away team was the team and the match was in the FA Cup's group stage.

    Args:
    season_id: The season of the FA Cup competition. This is a foreign key to the Season model.
    team_id: The team in the FA Cup competition. This is a foreign key to the Team model.
    gender: Men's or women's FA Cup competition?

    Returns:
        The number of goals conceded by the team in the FA Cup's group stage.
    """
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    stage = Stage.objects.get(name="Group Stage")
    competition = Competition.objects.get(
        name = "FA Cup",
        gender = gender
    )

    # Get the sum of away team score when the home team is the given team
    away_goals_conceded = Match.objects.filter(
        home_team=team,
        competition = competition,
        stage = stage,
        match_day__season=season
    ).aggregate(Sum('away_team_score'))['away_team_score__sum'] or 0

    # Get the sum of home team score when the away team is the given team
    home_goals_conceded = Match.objects.filter(
        away_team=team,
        competition = competition,
        stage = stage,
        match_day__season=season
    ).aggregate(Sum('home_team_score'))['home_team_score__sum'] or 0

    # Calculate the total goals conceded
    total_goals_conceded = away_goals_conceded + home_goals_conceded

    return total_goals_conceded or 0

def get_team_no_of_fa_cup_group_stage_matches_played(season_id, team_id, gender):
    
    """Get the number of matches played by a team in an FA Cup.
    
    Args:
        season_id: The season of the FA Cup competition. This is a foreign key to the Season model.
        team_id: The team in the FA Cup competition. This is a foreign key to the Team model.
        gender: Men's or women's FA Cup competition?

    Returns:
        The number of matches played by team in an FA Cup.
    """
    
    team = Team.objects.get(id=team_id)
    season = Season.objects.get(id=season_id)
    stage = Stage.objects.get(name="Group Stage")
    competition = Competition.objects.get(
        name = "FA Cup",
        gender = gender
    )

    no_of_fa_cup_group_matches_played = Match.objects.filter(
        Q(match_day__season=season, competition=competition, home_team=team, stage=stage, has_started=True) |
        Q(match_day__season=season, competition=competition, away_team=team, stage=stage, has_started=True)
    ).count()
        

    return no_of_fa_cup_group_matches_played 



@api_view(['PATCH'])
def update_mens_league_standings(request, season_id):
    """See update_league_standings for documentation.
    
    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league standings. This is a foreign key to the Season model.
    
    """
    return update_league_standings(season_id, 'M')


@api_view(['PATCH'])
def update_womens_league_standings(request, season_id):
    """See update_league_standings for documentation.
    
    Args:
    A JSON request. The request must contain the following fields:
    season: The season of the league standings. This is a foreign key to the Season model.
    
    """
    return update_league_standings(season_id, 'W')

def update_mens_fa_cup_standings(season_id):
    
    """Update the standings for an FA Cup's group stage. This is a helper function. It finds the standings for the FA Cup, and updates the matches won, matches lost, goals for, goals against, and matches played for each team in the standings. These values are used to calculate other values like goal difference and matches drawn.
    
    Args:
    season_id_arg: The season of the FA Cup group standings. This is a foreign key to the Season model.
     
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Standings updated successfully' or 'Standings update failed'.
    """   
    try:         
        season = Season.objects.get(id=season_id)
        
        if not season:
            return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    

        # use filter because FA Cup always has two groups, A and B.
        standings = Standings.objects.filter(
            season = season,
            competition__name = 'FA Cup',
            competition__gender = 'M'
        )
        
        if not standings:
            return Response({'message': 'Standings not found. Perhaps there was no FA Cup competition during this season'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update values in both Groups A and B.
        for standing in standings:
        
            standings_teams = StandingsTeam.objects.filter(standings=standing)
            
            for standings_team in standings_teams:
                team = standings_team.team
                standings_team.matches_won = get_team_no_of_wins_in_fa_cup_group_stage(season_id, team.id, 'M')
                standings_team.matches_lost = get_team_no_of_losses_in_fa_cup_group_stage(season_id, team.id, 'M')
                standings_team.goals_for = get_team_no_of_goals_scored_in_fa_cup_group_stage(season_id, team.id, 'M')
                standings_team.goals_against = get_team_no_of_goals_conceded_in_fa_cup_group_stage(season_id, team.id, 'M')
                standings_team.matches_played = get_team_no_of_fa_cup_group_stage_matches_played(season_id, team.id, 'M')
                standings_team.save()
                
        return Response({'message': 'Standings updated successfully'}, status=status.HTTP_200_OK)
    
    except Standings.DoesNotExist:
        return Response({'message': 'Standings not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Season.DoesNotExist:
        return Response({'message': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'message': 'Standings update failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_latest_mens_standings(request):
    
    """Get the latest standings for a season and competition. It finds the latest season and competition, and returns the standings for the season and competition. If the latest season and competition is the FA Cup, it returns the FA Cup group standings. If the latest season and competition is the Premier League, it returns the Premier League standings.
    
    Args:
    A JSON request. The request does not contain any fields.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains the standings for the season and competition. The status code is either 200 or 404.
    """
    
    latest_season = Season.objects.latest('start_date')
    latest_season = Season.objects.latest('start_date')
    premier_league_comp = Competition.objects.get(
        name = 'Premier League',
        gender = 'M'
    )
    
    league_standings = get_league_standings(latest_season.id, premier_league_comp.id)
    fa_cup_standings = get_season_mens_fa_cup_group_standings_helper(latest_season.id)
    
    if league_standings.status_code == 404:
        return fa_cup_standings
    
    if fa_cup_standings.status_code == 404:
        return league_standings
    
    

def get_season_mens_fa_cup_group_standings_helper(season_id):
    """
    See get_season_mens_fa_cup_group_standings for documentation. This is a helper function and it's called by get_latest_mens_standings. It differs from get_season_mens_fa_cup_group_standings in that its argument is a season_id, not a request.
    
    """
       
    try:
        
        season = Season.objects.get(id=season_id)
        
        competition = Competition.objects.get(
            name='FA Cup',
            gender='M'
        )
        
        if not competition:
            return Response({'message': 'FA Cup not found'}, status=status.HTTP_404_NOT_FOUND)
        
        standings = Standings.objects.filter(
            season=season,
            competition=competition
        )
        
        if not standings:
            return Response({'message': 'FA Cup group standings not found'}, status=status.HTTP_404_NOT_FOUND)
        
        update_mens_fa_cup_standings(season_id)
        
        serializer = StandingsSerializer(standings, many=True)
        
        return Response({'data': serializer.data, 'message': 'FA Cup group standings retrieved'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'An error occurred', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['DELETE'])
def delete_standings(request, standings_id):
    """Delete the standings for a season and competition. This is a helper function. It finds the standings for the season and competition, and deletes them.
    
    Args:
    season_id: The season of the standings. This is a foreign key to the Season model.
    competition_id: The competition of the standings. This is a foreign key to the Competition model.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Standings deleted successfully' or 'Standings deletion failed'.
    """
    
    try:
        standings = Standings.objects.get(
            id=standings_id
        )  
        
        standings.delete()
        
        return Response({'message': 'Standings deleted successfully'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Standings deletion failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)