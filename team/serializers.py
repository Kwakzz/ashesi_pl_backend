from team.models import Team
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Team
        fields = '__all__'
        
    def to_representation(self, instance):
        # When retrieving a team, include the players associated with the team.
        representation = super().to_representation(instance)
        # Extract the URL part from the "logo" field
        logo = representation.get('logo_url', '')
        representation['logo_url'] = self.extract_image_url(logo)
        cover_photo = representation.get('cover_photo_url', '')
        representation['cover_photo_url'] = self.extract_image_url(cover_photo)
        return representation
        
    
    def extract_image_url(self, value):
        # Check if "image/upload/" is present in the string
        if "image/upload/" in value:
            # Split the string based on "image/upload/" and keep the second part
            parts = value.split("image/upload/", 1)
            return parts[1]
        
        # If "image/upload/" is not present, return the original value
        return value
        
        
    