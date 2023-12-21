from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from team.models import Team
from team.serializers import TeamSerializer


@api_view(['POST'])
def create_team(request):
    
    """Create a new team. Its argument is a JSON request which is deserialized into a django model.
    
    Args:
    A JSON request. The request must contain the following fields:
    name: The name of the team.
    name_abbreviation: The abbreviated name of the team.
    logo_url: The url of the team's logo.
    color: The color of the team.
    twitter_url: The url of the team's twitter page.
    

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Team created successfully' or 'Team creation failed'.
    """
    
    serializer = TeamSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Team created successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Team creation failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PATCH'])
def update_team(request, id):
    """Update a team. Its argument is a JSON request which is deserialized into a django model.

    Args:
    A JSON request. The request can contain any combination of the following fields:
    name: The name of the team.
    name_abbreviation: The abbreviated name of the team.
    logo_url: The url of the team's logo.
    color: The color of the team.
    twitter_url: The url of the team's twitter page.
    
    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of errors if any. The message is either 'Team updated successfully' or 'Team update failed'.
    """
    
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Team updated successfully'}, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
def get_teams(request):
    """Get all teams.
    
    Args:
    None.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and a list of teams.
    """
    
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response({'message': 'Teams retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_team(request):
    """Get a team.

    Args:
    request: A get request. The request must contain the id of the team to be retrieved.

    Returns:
        A response object containing a JSON object and a status code. The JSON object contains a message and the team.
    """
    id_param = request.query_params.get('id')

    if not id_param:
        return Response({'message': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id = int(id_param)
    except ValueError:
        return Response({'message': 'Invalid Team ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team)
    return Response({'message': 'Team retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
