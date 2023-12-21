from player.models import Player, PlayerPosition
from rest_framework import serializers
from team.models import Team
from team.serializers import TeamSerializer
import re

class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerPosition
        fields = '__all__'


year_group_pattern = re.compile(r'^\d{4}$')

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
        return representation