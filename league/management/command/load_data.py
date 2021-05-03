from django.core.management.base import BaseCommand
from league.models import Team, Player, Match, Score

from django.contrib.auth.models import Group, User, Permission

class Command(BaseCommand):
    def _setup_data(self):
        #coach1
        coach=User.objects.create_user(username="profoak", email= "prof.oak@pokemon.com", password="palletttown123")
        #team1
        team=Team.objects.create(name="Team Kanto", coach=coach)
        #Player 1
        player_user1 = User.objects.create_user(username="ashKetchum", email="a.ketchum@pokemon.com", password="pickachu4Eva")
        palayer1 =Player.objects.create(name = player_user1, height="156", team = team)
        #Player 2
        player_user2 = User.objects.create_user(username="garyoaks", email="g.oaks@pokemon.com", password="ashsucks123")
        player2= Player.objects.create(name=player_user2, height="157", team = team)

        #coach2
        coach2=User.objects.create_user(username="chanadlerbong", email= "chanandler.bong@friend.com", password="transpondster")
        #team1
        team2=Team.objects.create(name="Team Friends", coach=coach2)
        #Player 1
        player_user_3 = player_user = User.objects.create_user(username="kenadams", email="k.adams@friend.com", password="foodsharingoff")
        player3 = Player.objects.create(name = player_user_3, height="170", team = team2)
        #Player 2
        player_user5 = User.objects.create_user(username="rejinaphalange", email="r.phalange@friend.com", password="coolauntpheobe")
        player5 =Player.objects.create(name=player_user5, height="160", team = team2)

        #match1
        match1 = Match.objects.create(team1=team, team2=team2, round=1, winner=team2)

        #scores_match1
        score1 = Score.objects.create(match=match1, player=palayer1, score=3)
        score2 = Score.objects.create(match=match1, player=player2, score=4)

        score3 = Score.objects.create(match=match1, player=player3, score=9)
        score4 = Score.objects.create(match=match1, player=player5, score=5)
    
    def _create_admin(self):
        admin=User.objects.create_user(username="winniethepooh", email="winni.pooh@something.com", password="honey1994")
    
    def _create_groups(self):
        group=Group(name="Coach")
        group.save()
        user=User.objects.get(username="profoak")
        user.groups.add(group)
        user=User.objects.get(username="chanadlerbong")
        user.groups.add(group)

        group=Group(name="LeagueAdmin")
        group.save()
        user=User.objects.get(username="winniethepooh")
        user.groups.add(group)

    def handle(self, *args, **options):
        self._setup_data()
        self._create_admin()
        self._create_groups()
    