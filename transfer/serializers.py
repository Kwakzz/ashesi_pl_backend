from rest_framework import serializers
from player.serializers import PlayerSerializer
from team.serializers import TeamSerializer
from transfer.models import Transfer

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a transfer, include the player, from_team and to_team associated with the transfer.
        representation = super().to_representation(instance)
        representation['player'] = PlayerSerializer(instance.player).data
        representation['from_team'] = TeamSerializer(instance.from_team).data
        representation['to_team'] = TeamSerializer(instance.to_team).data
        return representation
    
    def validate(self, data):
        # A player cannot be transferred to the same team he/she is already in
        if data['from_team'] == data['to_team']:
            raise serializers.ValidationError('A player cannot be transferred to the same team he/she is already in')
        return data