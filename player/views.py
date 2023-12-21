from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from player.models import Player, PlayerPosition
from player.serializers import PlayerSerializer, PlayerPositionSerializer


@api_view(['POST'])
def create_player_position(request):
    """Create a new player position. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the player position.
    name_abbreviation: The abbreviation of the player position.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Player position created successfully' or 'Player position creation failed'.
    """
    
    serializer = PlayerPositionSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Player position created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Player position creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_player(request):
    
    """Create a player. Its argument is a JSON request which is deserialized into a django model.
    
    Args:
    A JSON request. The request must contain the following fields:
    first_name: The first name of the player.
    last_name: The last name of the player.
    birth_date: The birth date of the player.
    position: The position of the player. This is a foreign key to the PlayerPosition model.
    gender: It's either M or W. M represents Men, and W, Women.
    year_group: The year group of the player.
    is_active: A boolean value indicating whether the player is active or not.
    team: The team the player belongs to. This is a foreign key to the Team model.
    
    

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Player created successfully' or 'Player creation failed'.
    """
    
    serializer = PlayerSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Player created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Player creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_player(request, id):
    """Update a player. Its argument is a JSON request which is deserialized into a Django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    first_name: The first name of the player.
    last_name: The last name of the player.
    birth_date: The birth date of the player.
    position: The position of the player. This is a foreign key to the PlayerPosition model.
    gender: It's either M or W. M represents Men, and W, Women.
    year_group: The year group of the player.
    is_active: A boolean value indicating whether the player is active or not.
    team: The team the player belongs to. This is a foreign key to the Team model.

    Returns:
    A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any.
    The message is either 'Player updated successfully' or 'Player update failed'.
    """
    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PlayerSerializer(player, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Player updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Player update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    
@api_view(['GET'])
def get_players(request):
    """Get all players.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a list of players.
    """
    
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_player(request):
    """Get a player.

    Args:
    request: A get request. The request must contain the id of the player to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the player.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Player ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Player ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PlayerSerializer(player)
    return Response({'message': 'Player retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)