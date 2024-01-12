import os
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from news.models import NewsItem, NewsItemTag
from news.serializers import NewsItemSerializer, NewsItemTagSerializer
from cloudinary.uploader import upload



@api_view(['POST'])
def create_news_item_tag(request):
    """Create a new news item tag. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the news item tag.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'News item tag created successfully' or 'News item tag creation failed'.
    """
    
    serializer = NewsItemTagSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'News item tag created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'News item tag creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_tags(request):
    """Get all news item tags.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of news item tags.
    """
    
    tags = NewsItemTag.objects.all()
    serializer = NewsItemTagSerializer(tags, many=True)
    return Response({'message': 'News item tags retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_news_item(request):
    """Create a new news item. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    featured_image: The bytes stream of the news item's featured image.
    title: The title of the news item.
    subtitle: The subtitle of the news item.
    pub_date: The date of publication of the news item.
    text: The text of the news item.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'News item created successfully' or 'News item creation failed'.
    """
    
    try:
        serializer = NewsItemSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # Upload the featured image to Cloudinary
            image_file = request.data.get('featured_image')
            
            if not image_file:
                return Response({'message': 'Featured image is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if image_file:
            
                cloudinary_response = upload(
                    image_file, 
                    folder=settings.CLOUDINARY_NEWS_IMAGE_FOLDER, 
                    api_key=settings.CLOUDINARY_API_KEY,
                    api_secret=settings.CLOUDINARY_API_SECRET,
                    cloud_name=settings.CLOUD_NAME
                )
                
                serializer.validated_data['featured_image'] = cloudinary_response['secure_url']

                serializer.save()

                return Response({'message': 'News item created successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({'message': 'News item creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'message': 'News item creation failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PATCH'])
def update_news_item(request, id):
    """Update a news item. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    featured_image: The url of the news item's featured image.
    title: The title of the news item.
    subtitle: The subtitle of the news item.
    pub_date: The date of publication of the news item.
    text: The text of the news item.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'News item updated successfully' or 'News item update failed'.
    """
    
    try:
        news_item = NewsItem.objects.get(id=id)
    except NewsItem.DoesNotExist:
        return Response({'message': 'News item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsItemSerializer(news_item, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'News item updated successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'message': 'News item update failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
def delete_news_item(request, id):
    """Delete a news item.

    Args:
    id: The id of the news item to be deleted.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'News item deleted successfully' or 'News item deletion failed'.
    """
    
    try:
        news_item = NewsItem.objects.get(id=id)
    except NewsItem.DoesNotExist:
        return Response({'message': 'News item not found'}, status=status.HTTP_404_NOT_FOUND)

    news_item.delete()
    return Response({'message': 'News item deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_news_items(request):
    """Get all news items.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of news items.
    """
    
    news_items = NewsItem.objects.all()
    serializer = NewsItemSerializer(news_items, many=True)
    return Response({'message': 'News items retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_news_item(request):
    """Get a news item.

    Args:
    request: A get request. The request must contain the id of the news item to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the news item.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'News item ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid News item ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        news_item = NewsItem.objects.get(id=id)
    except NewsItem.DoesNotExist:
        return Response({'message': 'News item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsItemSerializer(news_item)
    return Response({'message': 'News item retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)