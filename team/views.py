from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from serializer import TeamSerializer
from team.models import Team


class CreateTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        name = request.data.get('name')

        team = Team.objects.create(name=name, creator=request.user)

        team_serializer = TeamSerializer(team)

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": {team_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class UpdateTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        team_id = request.Get.get('team_id')

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

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": {team_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class DeleteTeam(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request):
        team_id = request.Get.get('team_id')

        team = Team.objects.get(pk=team_id, creator=request.user)

        team.delete()

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": {'team deleted'}
                         },
                        status=status.HTTP_200_OK)
