from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name=models.CharField(max_length=100)
    coach=models.ForeignKey(User, related_name="coach", on_delete=models.CASCADE)

class Player(models.Model):
    name=models.ForeignKey(User, related_name="player_name",on_delete=models.CASCADE)
    height=models.IntegerField()
    team=models.ForeignKey(Team, related_name="team", on_delete=models.CASCADE)

class Match(models.Model):
    team1=models.ForeignKey(Team, related_name="first_team", on_delete=models.CASCADE)
    team2=models.ForeignKey(Team, related_name="second_team", on_delete=models.CASCADE)
    round=models.IntegerField()
    winner=models.ForeignKey(Team, related_name="winner", on_delete=models.CASCADE)

class Score(models.Model):
    match=models.ForeignKey(Match, related_name="match", on_delete=models.CASCADE)
    player=models.ForeignKey(Player, related_name="player", on_delete=models.CASCADE)
    score=models.IntegerField()