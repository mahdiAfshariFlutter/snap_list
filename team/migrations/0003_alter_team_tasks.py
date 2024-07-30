# Generated by Django 5.0.3 on 2024-07-30 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_team_alter_task_assign_users'),
        ('team', '0002_alter_team_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='tasks',
            field=models.ManyToManyField(blank=True, default=24, related_name='teams', to='task.task'),
        ),
    ]
