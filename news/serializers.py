from rest_framework import serializers
from account.models import Fan
from account.serializers import FanSerializer

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
        return representation
    
