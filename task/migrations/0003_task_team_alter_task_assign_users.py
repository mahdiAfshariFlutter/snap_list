# Generated by Django 5.0.3 on 2024-07-30 06:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_type'),
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='team.team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='assign_users',
            field=models.ManyToManyField(blank=True, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
