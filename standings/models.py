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
    matches_played = models.PositiveIntegerField(blank=True, null=True, default=0)
    matches_won = models.PositiveIntegerField(blank=True, null=True, default=0)
    matches_drawn = models.PositiveIntegerField(blank=True, null=True, default=0)
    matches_lost = models.PositiveIntegerField(blank=True, null=True, default=0)
    goals_for = models.PositiveIntegerField(blank=True, null=True, default=0)
    goals_against = models.PositiveIntegerField(blank=True, null=True, default=0)
    goal_difference = models.IntegerField(blank=True, null=True, default=0)
    points = models.IntegerField(blank=True, null=True, default=0)
    
    def calculate_derived_values(self):
        self.goal_difference = self.goals_for - self.goals_against
        self.matches_drawn = self.matches_played - self.matches_won - self.matches_lost
        self.points = 3 * self.matches_won + self.matches_drawn
        
    def save(self, *args, **kwargs):
        self.calculate_derived_values()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.standings.name + ' - ' + self.team.name + ' - ' + str(self.position)
    
    class Meta:
        unique_together = ('standings', 'team')
        ordering = ['points', 'goal_difference', 'goals_for', 'team__name']
    