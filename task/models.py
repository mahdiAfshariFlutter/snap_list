from django.db import models

from User.models import User
from team.models import Team


class Task(models.Model):
    Priority = (
        ('Low', "low"),
        ('Normal', 'normal'),
        ('High', 'high'),
    )
    Type = (
        ('Published', 'published'),
        ('Archive', 'archive'),
    )
    title = models.CharField(max_length=25)
    priority = models.CharField(max_length=25, choices=Priority, default='Low')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    doe_date = models.DateTimeField(null=True, blank=True)
    assign_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    type = models.CharField(max_length=25, choices=Type, default='Published')
