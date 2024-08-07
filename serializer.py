from rest_framework import serializers

from User.models import User
from task.models import Task
from team.models import Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar']


class TaskDetailDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'creator', 'is_done', 'doe_date', 'assign_users',
                  'type', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    tasks = TaskDetailDetailSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'tasks', 'pinned', 'created_at', 'updated_at', 'creator']


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    team = TeamDetailSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'creator', 'is_done', 'doe_date', 'assign_users',
                  'type', 'created_at', 'team']
