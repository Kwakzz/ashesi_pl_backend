from account.models import Fan
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from team.models import Team
from team.serializers import TeamSerializer

class FanSerializer (serializers.ModelSerializer):
    
    # password cannot be read. Meaning, when the get method is called, it's not included in the returned fields.
    # password is also validated with Django's in-built validate_password function 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    class Meta:
        model = Fan
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_no', 'birth_date', 'is_active', 'fav_team')
          

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)