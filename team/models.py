from django.db import models

from User.models import User


class Team(models.Model):
    name = models.CharField(max_length=25)
    tasks = models.ManyToManyField('task.Task', blank=True, related_name='teams')
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
