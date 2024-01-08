from django.db import models

# Create your models here.
class Transfer (models.Model):
    player= name = models.ForeignKey('player.Player', related_name='transfers', on_delete=models.CASCADE)
    from_team = models.ForeignKey('team.Team', related_name='transfers_out', on_delete=models.CASCADE)
    to_team = models.ForeignKey('team.Team', related_name='transfers_in', on_delete=models.CASCADE)
    date = models.DateField(auto_add_now=True)
    
    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name + ' moved from ' + self.from_team.name + ' to ' + self.to_team.name + ' on ' + self.date