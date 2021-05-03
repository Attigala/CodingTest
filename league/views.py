from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Team, Match, Player, Score
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core import serializers
from itertools import chain
from django.db.models import Sum,Avg,Count
import json
# Create your views here.
def home(request):
    if(request.user.is_authenticated):
        matches =Match.objects.all()
        serialized_matches = serializers.serialize('python', matches)
        return JsonResponse(serialized_matches, safe=False)
    else: 
        return HttpResponse(status=403)

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

def all_teams(request):
    if(request.user.is_authenticated):
        if(request.user.groups.filter(name="LeagueAdmin").exists()):
            try:
                players = Player.objects.raw(''' SELECT sum(score.score) totscore, player.id, player.team_id
                from league_player player
                inner join league_score score on
                score.player_id = player.id
                group by player.id, player.team_id''')
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
def ninetieth_percentile(request):
    if(request.user.is_authenticated):
        if(request.user.groups.filter(name="Coach").exists()):
            teams=Team.objects.filter(coach=request.user)
            scores = Score.objects.raw(''' SELECT count(*) as count, score.id 
            FROM league_score score
            inner join league_player player ON
            player.id = score.player_id
            where player.team_id = %s
            group by score.id''', [teams.first().id])
            scoreCount = 0
            for score in scores:
                scoreCount = score.count
            #print(scoreCount)
            ninetiethPercentile = round(int(scoreCount) * 0.9)

            playerStats = Player.objects.raw(''' SELECT score.id, player.id as player_id, avg(score.score) averagescore
            FROM league_score score
            INNER JOIN league_player player ON
            player.id = score.player_id
            where player.team_id = %s 
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
