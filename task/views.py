from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from serializer import TaskSerializer
from task.models import Task


class CreateTask(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        title = request.data.get('title')

        task = Task.objects.create(title=title, creator=request.user)
        task_serializer = TaskSerializer(task)

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": {task_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class UpdateTask(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, task_id):

        title = request.data.get('title')
        is_done = request.data.get('is_done')
        priority = request.data.get('priority')

        task = Task.objects.get(pk=task_id, user=request.user)

        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        if is_done is not None:
            task.is_done = is_done

        task.save()

        task_serializer = TaskSerializer(task)

        return Response({"meta": {"status-code": 200, "message": "success"},
                         "data": {task_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class ArchivedTask(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, task_id):
        task = Task.objects.get(pk=task_id, user=request.user)
        task.type = 'Archive'
        task.save()
        task_serializer = TaskSerializer(task)
        return Response({"meta": {"status-code": 200, "message": "task Archived"},
                         "data": {task_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class DeleteTask(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, task_id):
        task = Task.objects.get(pk=task_id, user=request.user)
        task.delete()
        task_serializer = TaskSerializer(task)
        return Response({"meta": {"status-code": 200, "message": "task deleted"},
                         "data": {task_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class GetAllTasks(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        task_type = request.data.get('type')
        is_done = request.data.get('is_done')
        priority = request.data.get('priority')
        doe_date = request.data.get('doe_date')
        team_id = request.data.get('team_id')

        tasks = Task.objects.filter(user=request.user, type=task_type)

        if is_done:
            tasks = tasks.filter(is_done=is_done)
        if priority:
            tasks = tasks.filter(priority=priority)
        if doe_date:
            tasks = tasks.filter(doe_date=doe_date)
        if team_id:
            tasks = tasks.filter(team_id=team_id)

        task_serializer = TaskSerializer(tasks, many=True)
        return Response({"meta": {"status-code": 200, "message": "success", },
                         "data": {task_serializer.data}})
