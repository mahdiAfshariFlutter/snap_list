from django.contrib import admin

from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['creator', 'title', 'type']


admin.site.register(Task, TaskAdmin)
