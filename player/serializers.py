from fixture.models import Goal
from player.models import Player, PlayerPosition, Coach
from rest_framework import serializers
from team.models import Team
from team.serializers import TeamSerializer
import re
from django.utils import timezone
year_group_pattern = re.compile(r'^\d{4}$')

class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPosition
        fields = '__all__'



class PlayerSerializer(serializers.ModelSerializer):
    year_group = serializers.CharField(validators=[lambda x: year_group_pattern.match(x) is not None])
    class Meta:
        model = Player
        fields = '__all__'
        
        
    def to_representation(self, instance):
        # When retrieving a player, include the position and team associated with the player.
        representation = super().to_representation(instance)
        representation['position'] = PlayerPositionSerializer(instance.position).data
        representation['team'] = TeamSerializer(instance.team).data
        # player age = current year - year of birth
        representation['age'] = timezone.now().year - instance.birth_date.year
        # Extract the URL part from the "image" field
        if 'image' in representation and representation['image'] is not None:
            player_image = representation.get('image', '')
            representation['image'] = representation['image'].url
        
        # get no of goals scored in history
        goals = Goal.objects.filter(match_event__player=instance)
        representation['no_of_goals_in_history'] = len(goals)
        return representation
    
    def extract_image_url(self, value):
        # Check if "image/upload/" is present in the string
        if "image/upload/" in value:
            # Split the string based on "image/upload/" and keep the second part
            parts = value.split("image/upload/", 1)
            return parts[1]
        
        # If "image/upload/" is not present, return the original value
        return value
    
class CoachSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Coach
        fields = '__all__'
        
        
    def to_representation(self, instance):
        # When retrieving coach, include the team associated with the coach.
        representation = super().to_representation(instance)
        representation['team'] = TeamSerializer(instance.team).data
        return representation