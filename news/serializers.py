from rest_framework import serializers
from account.models import Fan
from account.serializers import FanSerializer
from django.utils.html import strip_tags
import bleach


from news.models import NewsItem, NewsItemTag

class NewsItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItemTag
        fields = '__all__'

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = '__all__'
    
    def to_representation(self, instance):
        # When retrieving a news item, include the tag associated with the news item.
        representation = super().to_representation(instance)
        representation['tag'] = NewsItemTagSerializer(instance.tag).data
        representation['author'] = FanSerializer(instance.author).data
        return representation
    
    def strip_html_tags(self, value):
        # Use bleach to strip HTML tags and handle special characters
        cleaned_value = bleach.clean(value, tags=[], strip=True)
        # Strip remaining HTML entities
        return strip_tags(cleaned_value)
    
    def create(self, validated_data):
        
        # Strip HTML tags from the title, subtitle and text fields
        validated_data['title'] = self.strip_html_tags(validated_data['title'])
        validated_data['subtitle'] = self.strip_html_tags(validated_data['subtitle'])
        validated_data['text'] = self.strip_html_tags(validated_data['text'])
        return super().create(validated_data)
        
    
