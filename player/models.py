from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class PlayerPosition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, default=None, unique=True)
    name_abbreviation = models.CharField(max_length=5, blank=False, null=False, default=None, unique=True)
    
    def __str__(self):
        return self.name
    
    
# Define default positions
DEFAULT_POSITIONS = [
    {'name': 'Forward', 'name_abbreviation': 'FWD'},
    {'name': 'Midfielder', 'name_abbreviation': 'MID'},
    {'name': 'Defender', 'name_abbreviation': 'DEF'},
    {'name': 'Goalkeeper', 'name_abbreviation': 'GK'},
]

# Signal handler to create default positions after migration
@receiver(post_migrate)
def create_default_positions(sender, **kwargs):
    if sender.name == 'player':
        for position_data in DEFAULT_POSITIONS:
            PlayerPosition.objects.get_or_create(**position_data)


class Player(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]
    
    MAJOR_CHOICES = [
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Computer Engineering'),
        ('BA', 'Business Administration'),
        ('MIS', 'Management Information Systems'),
    ]
        
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, null=False, blank=False, default=None)
    birth_date = models.DateField(blank=False, null=False)
    year_group = models.CharField(max_length=4, null=False, blank=False, default=None)
    major = models.CharField(max_length=150, null=False, blank=False, default=None, choices=MAJOR_CHOICES)
    is_active = models.BooleanField(default=True)
    team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='players', null=True, blank=True, default=None)
    position = models.ForeignKey(PlayerPosition, on_delete=models.SET_DEFAULT, related_name='players', null=True, blank=True, default=None)
    image = models.CharField(max_length=250, null=True, blank=True, default=None)

    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    
class Coach(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=100, null=False, blank=False, default=None)
    team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='coaches', null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, null=False, blank=False, default=None)