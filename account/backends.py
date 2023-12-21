# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        Fan = get_user_model()
        try:
            user = Fan.objects.get(email=email)
        except Fan.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
