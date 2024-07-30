from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from serializer import TeamSerializer, TeamDetailSerializer
from team.models import Team


class CreateTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        name = request.data.get('name')

        team = Team.objects.create(name=name, creator=request.user)

        team_serializer = TeamSerializer(team)

        return Response({"meta": {"status-code": 200, "message": "success , team created"},
                         "data": team_serializer.data
                         },
                        status=status.HTTP_200_OK)


class UpdateTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, team_id):
        name = request.data.get('name')
        pinned = request.data.get('pinned')

        team = Team.objects.get(pk=team_id, creator=request.user)

        if name is not None:
            team.name = name
        if pinned is not None:
            team.pinned = pinned

        team.updated_at = timezone.now()

        team.save()

        team_serializer = TeamSerializer(team)

        return Response({"meta": {"status-code": 200, "message": "success , team updated"},
                         "data": team_serializer.data
                         },
                        status=status.HTTP_200_OK)


class DeleteTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request,team_id):
        team = Team.objects.get(pk=team_id, creator=request.user)

        team.delete()

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": 'team deleted'
                         },
                        status=status.HTTP_200_OK)


class GetAllTeams(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        teams = Team.objects.filter(creator=request.user)

        paginator = Paginator(teams, per_page)
        try:
            teams_page = paginator.page(page)
        except PageNotAnInteger:
            teams_page = paginator.page(1)
        except EmptyPage:
            teams_page = paginator.page(paginator.num_pages)

        teams_serializer = TeamSerializer(teams_page, many=True)

        return Response({"meta": {"status-code": 200, "message": "success",
                                  "page": teams_page.number,
                                  "per_page": per_page,
                                  "last_page": paginator.num_pages
                                  },
                         "data": teams_serializer.data
                         },
                        status=status.HTTP_200_OK)
