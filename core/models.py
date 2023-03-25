from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg



class TCGroup(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TeamDirector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class TeamManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tc_group = models.ForeignKey(TCGroup, on_delete=models.CASCADE)
    manager = models.ForeignKey(TeamDirector, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class TeamCaptain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tc_group = models.ForeignKey(TCGroup, on_delete=models.CASCADE)
    manager = models.ForeignKey(TeamManager, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tc_group = models.ForeignKey(TCGroup, on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(TeamManager, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

    

class PhoneCall(models.Model):
    score = models.FloatField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, blank=True, null=True)
    team_captain = models.ForeignKey(TeamCaptain, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.agent and self.team_captain:
            raise ValueError("Either agent or team captain must be set for a phone call.")
        super().save(*args, **kwargs)
                


def get_agent_score(agent):
    phone_calls = PhoneCall.objects.filter(agent=agent)
    if phone_calls:
        return phone_calls.aggregate(Avg('score'))['score__avg']
    return None

def get_team_captain_score(team_captain):
    phone_calls = PhoneCall.objects.filter(team_captain=team_captain)
    if phone_calls:
        phone_calls_for_captain =  phone_calls.aggregate(Avg('score'))['score__avg']
    tc_group_agents = Agent.objects.filter(tc_group=team_captain.tc_group)
    agent_scores = [get_agent_score(agent) for agent in tc_group_agents if get_agent_score(agent) is not None]
    ans = sum(agent_scores)/len(agent_scores)
    xxx = phone_calls_for_captain + ans
    return  xxx/2 
   

def get_team_manager_score(team_manager):
    agents = Agent.objects.filter(manager=team_manager)
    tc_group_captains = TeamCaptain.objects.filter(tc_group=team_manager.tc_group)
    if agents or tc_group_captains:
        agent_scores = [get_agent_score(agent) for agent in agents if get_agent_score(agent) is not None]
        captain_scores = [get_team_captain_score(captain) for captain in tc_group_captains if get_team_captain_score(captain) is not None]
        avg_agent_score = sum(agent_scores) / len(agent_scores) if agent_scores else None
        avg_captain_score = sum(captain_scores) / len(captain_scores) if captain_scores else None
        team_manager_score = (avg_agent_score + avg_captain_score) / 2 if avg_agent_score and avg_captain_score else None
        # print("team manager score", team_manager_score)
        return team_manager_score
    return None

def get_team_director_score(team_director):
    team_managers = TeamManager.objects.filter(manager=team_director)
    if team_managers:
        manager_scores = [get_team_manager_score(manager) for manager in team_managers if get_team_manager_score(manager) is not None]
        avg_manager_score = sum(manager_scores) / len(manager_scores) if manager_scores else None
        # print("team director score", avg_manager_score)
        return avg_manager_score
    return None

