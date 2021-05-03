from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Team, Match, Player, Score
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core import serializers
from itertools import chain
from django.db.models import Sum,Avg,Count
import json

# If the user is successfully validated show them a list of matches
def home(request):
    if(request.user.is_authenticated):
        matches =Match.objects.all()
        serialized_matches = serializers.serialize('python', matches)
        return JsonResponse(serialized_matches, safe=False)
    else: 
        return HttpResponse(status=403)

# If the logged in user is a coach who is assigned to a team, show him his player's satistics
def team(request):
    if(request.user.is_authenticated):
        user=request.user

        try:
            teams=Team.objects.filter(coach=user)
            players=Score.objects.all().filter(player__team=teams.first()).select_related('player__name').annotate(average=Avg('score')).annotate(count=Count("player"))
            templist = list()
            for player in players:
                playerStat={
                    "playerName":player.player.name.username,
                    "totalMatches":player.count,
                    "averageScore":player.average
                }
                templist.append(playerStat)

            return JsonResponse(templist,safe=False)
        except Team.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=403)

#Show a league admin all the player's statistics
def all_teams(request):
    if(request.user.is_authenticated):
        if(request.user.groups.filter(name="LeagueAdmin").exists()):
            try:
                players = Player.objects.raw(''' SELECT sum(score.score) AS totscore, player.id, player.team_id
                FROM league_player player
                INNER JOIN league_score score ON
                score.player_id = player.id
                GROUP BY player.id, player.team_id''')
                tempList = list()
                for player in players:
                    teamStat={
                        "playername":player.id,
                        "team": player.team_id,
                        "totalscore":player.totscore
                    }
                    tempList.append(teamStat)
                return JsonResponse(tempList, safe=False)
            except Team.DoesNotExist:
                return HttpResponse(status= 404)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)

#Show the coach his best performing players
def ninetieth_percentile(request):
    if(request.user.is_authenticated):
        if(request.user.groups.filter(name="Coach").exists()):
            teams=Team.objects.filter(coach=request.user)
            scores = Score.objects.raw(''' SELECT count(*) AS count, score.id 
            FROM league_score score
            INNER JOIN league_player player ON
            player.id = score.player_id
            WHERE player.team_id = %s
            GROUP by score.id''', [teams.first().id])
            scoreCount = 0
            for score in scores:
                scoreCount = score.count
            ninetiethPercentile = round(int(scoreCount) * 0.9)

            playerStats = Player.objects.raw(''' SELECT score.id, player.id AS player_id, AVG(score.score) AS averagescore
            FROM league_score score
            INNER JOIN league_player player ON
            player.id = score.player_id
            WHERE player.team_id = %s 
            GROUP BY player.id, score.id
            ORDER BY score.score''', [teams.first().id])
            tempList = list()
            for index in range(scoreCount, len(playerStats)):
                playerStat = {
                    "playerId": playerStats[index].player_id,
                    "averageScore":playerStats[index].averagescore
                }
                tempList.append(playerStat)
            return JsonResponse(tempList, safe=False)
                        
    else:
        return HttpResponse(status=403)
