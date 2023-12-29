from fixture.serializers import CompetitionSerializer, SeasonSerializer
from standings.models import Standings, StandingsTeam
from rest_framework import serializers
import re
from django.utils import timezone

from team.serializers import TeamSerializer

class StandingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standings
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a standings, include the season and competition associated with the standings.
        representation = super().to_representation(instance)
        representation['season'] = SeasonSerializer(instance.season).data
        representation['competition'] = CompetitionSerializer(instance.competition).data
        
        standings_teams = StandingsTeam.objects.filter(standings=instance)
        
        # sort the standings teams by points, goal difference, goals for, and team name
        standings_teams = sorted(standings_teams, key=lambda x: (x.points, x.goal_difference, x.goals_for, x.team.name), reverse=True)
        representation['standings_teams'] = StandingsTeamSerializer(standings_teams, many=True).data
        return representation
    
    
class StandingsTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandingsTeam
        fields = '__all__'
        
        
    def to_representation(self, instance):
        # When retrieving a standings team, include the team associated with the standings team.
        representation = super().to_representation(instance)
        representation['team'] = TeamSerializer(instance.team).data
        return representation
