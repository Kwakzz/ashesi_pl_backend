from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, default=None, unique=True)
    name_abbreviation = models.CharField(max_length=5, blank=False, null=False, default=None, unique=True)
    logo_url = models.URLField(max_length=200, null=False, blank=False, default=None)
    cover_photo_url = models.URLField(max_length=250, null=False, blank=False, default=None)
    color = models.CharField(max_length=20, null=False, blank=False, default=None)
    twitter_url = models.URLField(max_length=100, null=False, blank=False, default=None, unique=True,)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name    


# create default teams

DEFAULT_TEAMS = [
    {'name': 'Elite', 'name_abbreviation': 'ELI', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097680/Team%20Logos/elite_logo_pmbtg5.png', 'color': '121354', 'twitter_url': 'https://twitter.com/elite1_fc', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/elite_cover_eqamaq.jpg'},
    
    {'name': 'Legends United', 'name_abbreviation': 'LU', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097681/Team%20Logos/lu_logo_oailhh.png', 'color': '000000', 'twitter_url': 'https://twitter.com/LUFCau', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/lu_cover_u14czk.jpg'},
    
    {'name': 'Highlanders', 'name_abbreviation': 'HIG', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097681/Team%20Logos/highlanders_logo_yu8c40.png', 'color': 'a79958', 'twitter_url': 'https://twitter.com/Highlandersoff1', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/highlanders_cover_oxuhrh.jpg'},
    
    {'name': 'Kasanoma', 'name_abbreviation': 'KAS', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097680/Team%20Logos/kasanoma_logo_tatjsp.png', 'color': '0b6667', 'twitter_url': 'https://twitter.com/FcKasanoma', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/kasanoma_cover_sktsel.jpg'},
    
    {'name': 'Northside', 'name_abbreviation': 'NOR', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097681/Team%20Logos/northside_logo_wyy3lm.png', 'color': '241e20', 'twitter_url': 'https://twitter.com/NorthsideFooty', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/northside_cover_uifvth.jpg'},
    
    {'name': 'Red Army', 'name_abbreviation': 'RAR', 'logo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703097681/Team%20Logos/red_army_logo_yg9lym.png', 'color': 'e8272c', 'twitter_url': 'https://twitter.com/officalRedArmy', 'cover_photo_url': 'https://res.cloudinary.com/dvghxq3ba/image/upload/v1703250250/Team%20Cover%20Images/red_army_cover_cwyem6.jpg'},
]

@receiver(post_migrate)
def create_default_teams(sender, **kwargs):
    if sender.name == 'team':
        for team_data in DEFAULT_TEAMS:
            Team.objects.get_or_create(**team_data)
            
            