from django.db import models

from User.models import User
from task.models import Task


class Team(models.Model):
    name = models.CharField(max_length=25)
    tasks = models.ManyToManyField(Task, blank=True)
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
