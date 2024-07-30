from django.urls import path

from task.views import CreateTask, UpdateTask, DeleteTask, ArchivedTask, GetAllTasks

urlpatterns = [
    path('create_task/<int:team_id>/', CreateTask.as_view()),
    path('update_task/<int:task_id>/', UpdateTask.as_view()),
    path('delete_task/<int:task_id>/', DeleteTask.as_view()),
    path('archived_task/<int:task_id>/', ArchivedTask.as_view()),
    path('tasks/', GetAllTasks.as_view()),
]
