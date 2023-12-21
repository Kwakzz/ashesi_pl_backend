from fixture.models import ManOfTheMatch, Referee, Season, Competition, MatchDay, Match, MatchEvent, Stage, Goal, Substitution, StartingXI
from rest_framework import serializers
from player.models import Player
from player.serializers import PlayerSerializer
from team.models import Team

from team.serializers import TeamSerializer

class RefereeSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Referee
        fields = '__all__'
        
        
class SeasonSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Season
        fields = '__all__'
            
class CompetitionSerializer(serializers.ModelSerializer):
                
    class Meta:
        model = Competition
        fields = '__all__'
            
            
class MatchDaySerializer(serializers.ModelSerializer):
    
    # ensure match day date is within the season's start and end dates
    def validate(self, data):
        season = data.get('season')
        if season and (data['date'] < season.start_date or data['date'] > season.end_date):
            raise serializers.ValidationError({'date': 'Match day date should be within the season start and end dates.'})
        return data
    
    class Meta:
        model = MatchDay
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a match day, include the season associated with the match day.
        representation = super().to_representation(instance)
        representation['season'] = SeasonSerializer(instance.season).data
        return representation
    
class StageSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Stage
        fields = '__all__'
            
            
class MatchSerializer(serializers.ModelSerializer):
    
    # set required fields
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    match_day = serializers.PrimaryKeyRelatedField(queryset=MatchDay.objects.all(), required=True)
    competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), required=True)
    referee = serializers.PrimaryKeyRelatedField(queryset=Referee.objects.all(), required=True)
    match_time = serializers.TimeField(required=True)
    
    #ensure home team and away team are different
    def validate(self, data):
        if data['home_team'] == data['away_team']:
            raise serializers.ValidationError({'home_team': 'Home team and away team cannot be the same.'})
        return data

    class Meta:
        model = Match
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a match, include the home team, away team, match day, competition, referee and stage associated with the match.
        representation = super().to_representation(instance)
        representation['home_team'] = TeamSerializer(instance.home_team).data
        representation['away_team'] = TeamSerializer(instance.away_team).data
        representation['match_day'] = MatchDaySerializer(instance.match_day).data
        representation['competition'] = CompetitionSerializer(instance.competition).data
        representation['referee'] = RefereeSerializer(instance.referee).data
        
        # Conditionally include 'stage' only if it's not None
        if instance.stage:
            representation['stage'] = StageSerializer(instance.stage).data
        else:
            representation['stage'] = None
        return representation
    
    
class MatchEventSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = MatchEvent
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a match event, include the match and the player associated with the match event.
        representation = super().to_representation(instance)
        representation['match'] = MatchSerializer(instance.match).data
        representation['player'] = TeamSerializer(instance.player).data
        return representation
    
        
        
class GoalSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Goal
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a goal, include the match event, scoring team and assist provider associated with the goal.
        representation = super().to_representation(instance)
        representation['match_event'] = MatchEventSerializer(instance.match_event).data
        representation['scoring_team'] = TeamSerializer(instance.scoring_team).data
        representation['assist_provider'] = TeamSerializer(instance.assist_provider).data
        return representation
        

class SubstitutionSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Substitution
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a substitution, include the match event, player out and player in associated with the substitution.
        representation = super().to_representation(instance)
        representation['match_event'] = MatchEventSerializer(instance.match_event).data
        representation['player_out'] = TeamSerializer(instance.player_out).data
        representation['player_in'] = TeamSerializer(instance.player_in).data
        return representation
            

class StartingXISerializer(serializers.ModelSerializer):
                    
    class Meta:
        model = StartingXI
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a starting XI, include the match and all players associated with the starting XI.
        representation = super().to_representation(instance)
        representation['match'] = MatchSerializer(instance.match).data
        
        # Include player data for all players
        player_data = representation.pop('players')
        representation['players'] = PlayerSerializer(player_data, many=True).data
        
        return representation
    
    
class MatchEventWithGoalSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = MatchEvent
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a match event, include the match, player and goal associated with the match event.
        representation = super().to_representation(instance)
        representation['match_event'] = MatchEventSerializer(instance.match_event).data
        # representation['match'] = MatchSerializer(instance.match).data
        # representation['player'] = TeamSerializer(instance.player).data
        
        # Conditionally include 'goal' only if it's not None
        if instance.goal:
            representation['goal'] = GoalSerializer(instance.goal).data
        else:
            representation['goal'] = None
        return representation 

        
    
class MatchEventWithSubstitutionSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = MatchEvent
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a match event, include the match, player and substitution associated with the match event.
        representation = super().to_representation(instance)
        representation['match'] = MatchSerializer(instance.match).data
        representation['player'] = TeamSerializer(instance.player).data
        
        # Conditionally include 'substitution' only if it's not None
        if instance.substitution:
            representation['substitution'] = SubstitutionSerializer(instance.substitution).data
        else:
            representation['substitution'] = None
        return representation
        

class ManOfTheMatchSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = ManOfTheMatch
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['match'] = MatchSerializer(instance.match).data
        representation['player'] = TeamSerializer(instance.player).data
        
        return representation
    
    
    
    