from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from player.models import Player, PlayerPosition
from player.serializers import PlayerSerializer, PlayerPositionSerializer
from transfer.models import Transfer
from transfer.serializers import TransferSerializer

@api_view(['POST'])
def create_transfer(request):
    """Create a new transfer. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request must contain the following fields:
    player: The player being transferred.
    from_team: The team the player is being transferred from.
    to_team: The team the player is being transferred to.
    date: The date of the transfer.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Transfer created successfully' or 'Transfer creation failed'.
    """
    
    serializer = TransferSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        
        # Update the player's team
        player = Player.objects.get(id=request.data['player'])
        player.team = serializer.data['to_team']
        player.save()
        
        return Response({'message': 'Transfer created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Transfer creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_transfers(request):
    """Get all transfers.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of transfers.
    """
    
    transfers = Transfer.objects.all()
    serializer = TransferSerializer(transfers, many=True)
    return Response({'message': 'Transfers retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)