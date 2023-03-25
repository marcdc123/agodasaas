from django.contrib import admin
from .models import TCGroup, TeamDirector, TeamManager, TeamCaptain, Agent, PhoneCall


class PhoneCallAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'agent', 'team_captain')
    list_filter = ('agent__tc_group', 'team_captain__tc_group', 'score')
    search_fields = ('agent__user__username', 'team_captain__user__username')


admin.site.register(TCGroup)
admin.site.register(TeamDirector)
admin.site.register(TeamManager)
admin.site.register(TeamCaptain)
admin.site.register(Agent)
admin.site.register(PhoneCall, PhoneCallAdmin)
