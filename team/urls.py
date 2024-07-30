from django.urls import path

from team.views import CreateTeam, UpdateTeam, DeleteTeam, GetAllTeams

urlpatterns = [
    path('create_team/', CreateTeam.as_view()),
    path('update_team/<int:team_id>/', UpdateTeam.as_view()),
    path('delete_team/<int:team_id>/', DeleteTeam.as_view()),
    path('teams/', GetAllTeams.as_view()),
]
