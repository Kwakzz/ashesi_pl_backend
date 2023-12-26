from django.db import models

class Standings(models.Model):
    
    season = models.ForeignKey('fixture.Season', on_delete=models.CASCADE, related_name='standings')
    competition = models.ForeignKey('fixture.Competition', on_delete=models.CASCADE, related_name='standings')
    name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name
    
    
class StandingsTeam (models.Model):
    
    standings = models.ForeignKey('Standings', on_delete=models.CASCADE, related_name='standings_teams')
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='standings_teams')
    position = models.PositiveIntegerField()
    matches_played = models.PositiveIntegerField()
    matches_won = models.PositiveIntegerField()
    matches_drawn = models.PositiveIntegerField()
    matches_lost = models.PositiveIntegerField()
    goals_for = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    goal_difference = models.IntegerField()
    points = models.IntegerField()
    
    def __str__(self):
        return self.standings.name + ' - ' + self.team.name + ' - ' + str(self.position)
    
    class Meta:
        unique_together = ('standings', 'team')
        ordering = ['position']
    