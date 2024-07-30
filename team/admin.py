from django.contrib import admin

from team.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creator_username']
    list_display_links = ['name', 'creator_username']

    def creator_username(self, obj):
        return obj.creator.username


admin.site.register(Team, TeamAdmin)
