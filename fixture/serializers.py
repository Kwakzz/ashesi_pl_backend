from fixture.models import ManOfTheMatch, Referee, Season, Competition, MatchDay, Match, MatchEvent, Stage, Goal, Substitution, StartingXI
from rest_framework import serializers
from player.models import Player
from player.serializers import PlayerSerializer
from team.models import Team
from django.utils import timezone


from team.serializers import TeamSerializer

class RefereeSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Referee
        fields = '__all__'
        
        
class SeasonSerializer(serializers.ModelSerializer):
            
    class Meta:
        model = Season
        fields = '__all__'
        
    # ensure start date is before end date
    # ensure start date is not before today
    def validate(self, data):
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError({'start_date': 'Start date must be before end date.'})
            if start_date < timezone.now().date():
                raise serializers.ValidationError({'start_date': 'Start date cannot be before today.'})

        return data

            
class CompetitionSerializer(serializers.ModelSerializer):
                
    class Meta:
        model = Competition
        fields = '__all__'
            
            
class MatchDaySerializer(serializers.ModelSerializer):
    
    # ensure match day date is within the season's start and end dates.
    
    def validate(self, data):
        season = data.get('season')
        date = data.get('date')
        if season:
            season = Season.objects.get(id=season.id)
            if date:
                if date < season.start_date:
                    raise serializers.ValidationError({'date': 'Match day date cannot be before season start date.'})
                if date > season.end_date:
                    raise serializers.ValidationError({'date': 'Match day date cannot be after season end date.'})
            
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
    
    class Meta:
        model = Match
        fields = '__all__'
        
    # set required fields
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    away_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=True)
    match_day = serializers.PrimaryKeyRelatedField(queryset=MatchDay.objects.all(), required=True)
    competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), required=True)
    referee = serializers.PrimaryKeyRelatedField(queryset=Referee.objects.all(), required=True)
    match_time = serializers.TimeField(required=True)
    
    
    #ensure home team and away team are different
    # also ensure has_started and has_ended are not set to true if the match day date has not been reached
    def validate(self, data):
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        match_day = data.get('match_day')
        has_started = data.get('has_started')
        has_ended = data.get('has_ended')
        
        if home_team and away_team:
            if home_team == away_team:
                raise serializers.ValidationError({'home_team': 'Home team and away team cannot be the same.'})
            
        if match_day:
            match_day = MatchDay.objects.get(id=match_day.id)
            if match_day.date > timezone.now().date():
                if has_started:
                    raise serializers.ValidationError({'has_started': 'Match cannot have started if match day date has not been reached.'})
                if has_ended:
                    raise serializers.ValidationError({'has_ended': 'Match cannot have ended if match day date has not been reached.'})

        return data
    
        
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
        representation['player'] = PlayerSerializer(instance.player).data
        representation['team'] = TeamSerializer(instance.team).data
        
        if instance.event_type == 'Goal':
            # Check if there is a related goal and include additional fields
            if hasattr(instance, 'goal'):
                if instance.goal.assist_provider:
                    representation['assist_provider'] = PlayerSerializer(instance.goal.assist_provider).data
        
        return representation
        
    
        
        
class GoalSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Goal
        fields = '__all__'
        
    
        
    def to_representation(self, instance):
        # When retrieving a goal, include the match event, scoring team and assist provider associated with the goal.
        representation = super().to_representation(instance)
        representation['match_event'] = MatchEventSerializer(instance.match_event).data
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
    
        

class ManOfTheMatchSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = ManOfTheMatch
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['match'] = MatchSerializer(instance.match).data
        representation['player'] = TeamSerializer(instance.player).data
        
        return representation
    
    
    
    