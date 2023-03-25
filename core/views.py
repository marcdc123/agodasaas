from django.shortcuts import render
from .models import *
from django.db import connection


def getpeoplescore(user):
        if hasattr(user, 'agent'):
            score = get_agent_score(user.agent)
            return {'user': user.username, 'score': score}
        elif hasattr(user, 'teamcaptain'):
            score = get_team_captain_score(user.teamcaptain)
            return {'user': user.username, 'score': score}
        elif hasattr(user, 'teammanager'):
            score = get_team_manager_score(user.teammanager)
            return {'user': user.username, 'score': score}
        elif hasattr(user, 'teamdirector'):
            score = get_team_director_score(user.teamdirector)
            return {'user': user.username, 'score': score}
        else:
            return {'user': user.username, 'score': None}


def getagentsscore(request):
    user_scores = []
    for user in User.objects.all():
        score_dict = getpeoplescore(user)
        
        user_scores.append(score_dict)
    return render(request, 'core/score_table.html', {'user_scores': user_scores})

