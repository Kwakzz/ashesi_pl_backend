from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Referee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    last_name = models.CharField(max_length=50, null=False, blank=False, default=None)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Season(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, default=None, unique=True)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    
    def __str__(self):
        return self.name
        
class Competition(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, default=None)
    gender = models.CharField(max_length=1, null=False, blank=False, default=None, choices = GENDER_CHOICES)
    
    def __str__(self):
        return self.name + "(" + self.gender + ")"
    
DEFAULT_COMPETITIONS = [
    # MEN'S COMPETITIONS
    {'name': 'Champions League', 'gender': 'M'},
    {'name': 'FA Cup', 'gender': 'M'},
    {'name': 'Premier League', 'gender': 'M'},
    
    #WOMEN'S COMPETIITONS
    {'name': 'Champions League', 'gender': 'W'},
    {'name': 'FA Cup', 'gender': 'W'},
    {'name': 'Premier League', 'gender': 'W'},
    
]

@receiver(post_migrate)
def create_default_competitions(sender, **kwargs):
    if sender.name == 'fixture':
        for competition_data in DEFAULT_COMPETITIONS:
            Competition.objects.get_or_create(**competition_data)


    
class MatchDay(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(null=False, blank=False)
    date = models.DateField(blank=False, null=False)
    season = models.ForeignKey(Season, on_delete=models.SET_DEFAULT, related_name='match_days', null=True, blank=True, default=None)
    
    def __str__(self):
        return self.season.name + " - Match Day " + str(self.number)
    
    class Meta:
        ordering = ['date']

    
class Stage(models.Model):
    
    STAGE_CHOICES = [
        ('Group Stage', 'Group Stage'),
        ('Round of 16', 'Round of 16'),
        ('Quarter Finals', 'Quarter Finals'),
        ('Semi Finals', 'Semi Finals'),
        ('Finals', 'Finals')
    ]
    
    name = models.CharField(max_length=50, null=False, blank=False, default=None, unique=True)
    
DEFAULT_STAGES = [
    {'name': 'Group Stage'},
    {'name': 'Round of 16'},
    {'name': 'Quarter Finals'},
    {'name': 'Semi Finals'},
    {'name': 'Finals'}
]

@receiver(post_migrate)
def create_default_stages(sender, **kwargs):
    if sender.name == 'fixture':
        for stage_data in DEFAULT_STAGES:
            Stage.objects.get_or_create(**stage_data)
    
    
class Match (models.Model):
    id = models.AutoField(primary_key=True)
    home_team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='home_matches', null=False, blank=False, default=None)
    away_team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='away_matches', null=False, blank=False, default=None)
    match_day = models.ForeignKey(MatchDay, on_delete=models.SET_DEFAULT, related_name='matches', null=False, blank=False, default=None)
    competition = models.ForeignKey(Competition, on_delete=models.SET_DEFAULT, related_name='matches', null=False, blank=False, default=None)
    home_team_score = models.IntegerField(null=True, blank=True, default=0)
    away_team_score = models.IntegerField(null=True, blank=True, default=0)
    match_time = models.TimeField(blank=False, null=False, default=None)
    referee = models.ForeignKey(Referee, on_delete=models.SET_DEFAULT, related_name='matches', null=False, blank=False, default=None)
    stage = models.ForeignKey(Stage, on_delete=models.SET_DEFAULT, related_name='matches', null=True, blank=True, default=None)
    has_started = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)
    
    def __str__(self):
        return self.home_team.name + " vs " + self.away_team.name + " (" + self.competition.name + ")"
    
    class Meta:
        ordering = ['match_time']
        
        
class MatchEvent(models.Model):
        
    EVENT_TYPE_CHOICES = [
        ('Goal', 'Goal'),
        ('Yellow Card', 'Yellow Card'),
        ('Red Card', 'Red Card'),
        ('Substitution', 'Substitution'),
    ]
    
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.SET_DEFAULT, related_name='events', null=True, blank=True, default=None)
    event_type = models.CharField(max_length=50, null=False, blank=False, default=None, choices=EVENT_TYPE_CHOICES)
    player = models.ForeignKey('player.Player', on_delete=models.SET_DEFAULT, related_name='events', null=True, blank=True, default=None)
    minute = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return self.event_type + " - " + self.player.first_name + " " + self.player.last_name + " (" + self.match.home_team.name + " vs " + self.match.away_team.name + ")"
    
    class Meta:
        ordering = ['minute']
            

class Goal(models.Model):
    match_event = models.OneToOneField(MatchEvent, on_delete=models.CASCADE, related_name='goal')
    scoring_team = models.ForeignKey('team.Team', on_delete=models.SET_DEFAULT, related_name='scored_goals', null=True, blank=True, default=None)
    assist_provider = models.ForeignKey('player.Player', on_delete=models.SET_DEFAULT, related_name='assists', null=True, blank=True, default=None)
    
    def __str__(self):
        return self.match_event.player.first_name + " " + self.match_event.player.last_name + " (" + self.match_event.match.home_team.name + " vs " + self.match_event.match.away_team.name + ")"
    

class Substitution(models.Model):
    match_event = models.OneToOneField(MatchEvent, on_delete=models.CASCADE, related_name='substitution')
    player_out = models.ForeignKey('player.Player', on_delete=models.SET_DEFAULT, related_name='substitutions_out', null=True, blank=True, default=None)
    player_in = models.ForeignKey('player.Player', on_delete=models.SET_DEFAULT, related_name='substitutions_in', null=True, blank=True, default=None)
    
    
class ManOfTheMatch(models.Model):
    player = models.ForeignKey('player.Player', on_delete=models.SET_DEFAULT, related_name='players', null=False, blank=False, default=None)
    match = models.ForeignKey(Match, on_delete=models.SET_DEFAULT, related_name='matches', null=False, blank=False, default=None)
    
    def __str__(self):
        return self.player.first_name + " " + self.player.last_name + " (" + self.match.home_team.name + " vs " + self.match.away_team.name + ")"
    
    class Meta:
        ordering = ['match']
        

class StartingXI(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='starting_xis')
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    players = models.ManyToManyField('player.Player', related_name='starting_xis')

    def __str__(self):
        return f"Starting XI for {self.team.name} in {self.match}"

    class Meta:
        unique_together = ['match', 'team']