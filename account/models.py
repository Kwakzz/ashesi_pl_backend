from django.db import models
from django.contrib.auth.models import AbstractUser
from account.managers import CustomUserManager


class Fan(AbstractUser):
    id = models.AutoField(primary_key=True)
    birth_date = models.DateField(blank=False, null=False)
    phone_no = models.CharField(max_length=50, null=False, default=None, unique=True)
    is_active = models.BooleanField(default=False)
    fav_team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='fans', null=False, blank=False, default=None)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username
