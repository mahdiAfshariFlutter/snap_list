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

    def put(self, request, *args, **kwargs):

        task_id = request.Get.get('task_id')
        title = request.data.get('title')
        is_done = request.data.get('is_done')
        priority = request.data.get('priority')

        task = Task.objects.get(pk=task_id)

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
