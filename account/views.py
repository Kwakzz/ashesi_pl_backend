from django.utils import timezone
from django.conf import settings
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from account.models import Fan
from account.serializers import FanSerializer
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_str




@api_view(['POST'])
def register(request):
    
    """Register a new user. Its argument is a JSON request which is deserialized into a django model.
    The FanSerializer validates the user password and checks for constraint violations. If password validation
    yields a positive result, the password is hashed, and the user is saved,
    
    Args:
    A JSON request. The request must contain the following fields:
    username: The username of the user.
    first_name: The first name of the user.
    last_name: The last name of the user.
    email: The email of the user.
    password: The password of the user.
    phone_no: The phone number of the user.
    birth_date: The birth date of the user. 

    Returns:
        Response: A response object containing a JSON object and a status code.
        The JSON object contains a message and a list of errors if any. The message is either 'Fan registered successfully' or 'Fan registration failed'.
    """
    
    serializer = FanSerializer(data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Fan registered successfully'}, status=status.HTTP_201_CREATED)
    
    else:
        return Response({'message': 'Fan registration failed', 'errors': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    
   

@api_view(['POST'])
def sign_in(request):
    
    """Sign in a user. Its argument is a JSON request which is deserialized into a django model.
    
    Args:
    A JSON request. The request must contain the following fields:
    email: The email of the user.
    password: The password of the user.

    Returns:
        Response: A response object containing a JSON object and a status code.
        The JSON object contains a message, a data field and a list of errors if any. The message is either 'Login successful' or 'Login failed'. The data field contains the user's id, username, email, phone number and birth date.
    """
    
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:

        # authenticate returns a user object if the credentials are valid. Otherwise, it returns None.
        # it matches the password and email against that of the user, AUTH_USER_MODEL. AUTH_USER_MODEL is set in settings.py
        user = authenticate(request, email=email, password=password)

        if user is not None:
            
            if not user.is_active:
                return Response({'message': 'Account not activated'}, status=400)
            
            # get_or_create returns a tuple. first element is a token and second is a boolean indicating whether the token was created.
            token, created = Token.objects.get_or_create(user=user)
            
            if not created and token:
                # If the token already exists, delete it and create a new one
                token.delete()
                token = Token.objects.create(user=user)
            
            user.last_login = timezone.now()
            
            return Response({
                'token': token.key,
                'message': 'Login successful',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone_no': user.phone_no,
                    'birth_date': user.birth_date,
                    'fav_team_id': user.fav_team.id,
                    'fav_team': user.fav_team.name,
                }
            })
            
        else:
            # Invalid login credentials
            return Response({'message': 'Invalid login credentials'}, status=400)
        
    except Exception as e:
        return Response({'message': 'Login failed', 'error': str(e)}, status=400)
    
    
@api_view(['POST'])
def sign_out(request):
    """
    Sign out a user.
    The user's token is deleted from the database.
    
    Args:
        request: The request object containing the user's token.
        
    Returns:
        A response object containing a JSON object and a status code.
        The JSON object contains a message and a list of errors if any. The message is either 'Logout successful' or 'Logout failed'.
    """
    try:
        data = request.data
        token = data.get('token')
        token = Token.objects.get(key=token)
        token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Logout failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def send_activation_email(request):
    """
    Send an email to a user to activate his account.
    
    Args:
        request: The request object containing the user's email. The email is used to retrieve the user from the database. The user object is used to generate the activation link. The activation link is sent to the user's email.
    """
    try:
        
        data = request.data
        
        user = Fan.objects.get(email=data.get('email'))
        
        activation_link = generate_activation_link(user)
        
        subject = 'Activate Your APL Account'
        to_email = user.email

        # HTML content for the email
        html_message = render_to_string('activation_mail_template.html', {'activation_link': activation_link})

        # Plain text version of the HTML content for non-HTML email clients
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            html_message=html_message,  
        )
        
        return Response({'message': 'Activation email sent successfully'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'message': 'Activation email failed to send', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET'])
def activate_account(request):
    """
    Activate a user's account.
    The user's id is decoded from the base 64 encoded version. The user is retrieved from the database using the decoded id.
    The token is generated from the user object. If the token is valid, the user's account is activated.
    
    Args:
        request: The request object containing the encoded uid and token. These parameters are attached to the activation link.
        
    Returns:
        A response object containing a JSON object and a status code.
        The JSON object contains a message and a list of errors if any. The message is either 'Account activated successfully' or 'Account activation failed'.
    """
    try:
        
        data = request.query_params
        encoded_uid = data.get('uid')
        token = data.get('token')
         
        uid = force_str(urlsafe_base64_decode(encoded_uid))
        user = Fan.objects.get(id=uid)
        token = Token.objects.get(user=user)
        
        if token.key == data.get('token'):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'message': 'Account activation failed'}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({'message': 'Account activation failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
    
# HELPERS

def generate_token_and_encoded_uid(user):
    """
    Generate a token and a base 64 encoded version of the user's id. 
    The token is generated from the user object.
    The encoded uid is generated by encoding the user's id using urlsafe_base64_encode.
    The encoded uid and the token are used to generate an activation link.
    For example, https://apl/account/activate?uid=MTU&token=1jw-1a2-3b4
    
    Args:
        user: The user whose encoded uid and token are to be generated.
        
    Returns:
        A token generated from the user object and a base 64 encoded version of the user's id. The format is (token.key, encoded_uid). Note that token.key is a string, and token is an object, hence the need to access the key attribute.
    """
    token, created = Token.objects.get_or_create(user=user)  
    
    if not created and token:
        # If the token already exists, delete it and create a new one
        token.delete()
        token = Token.objects.create(user=user)
      
    encoded_uid = urlsafe_base64_encode(force_bytes(user.id))
    return token.key, encoded_uid


def generate_activation_link(user):
    """
    Generate an activation link for a user.
    The activation link contains a base 64 encoded version of the user's id and a token generated
    from the user object.
    
    Args:
        user: The user whose activation link is to be generated.
        
    Returns:
        A string containing the activation link.
    """
    token, encoded_uid = generate_token_and_encoded_uid(user)
    return f"http://{settings.BACKEND_URL}/account/activate?uid={encoded_uid}&token={token}"


