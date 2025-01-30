from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_name", "deadline", "executor", "status", "parent_task")
    search_fields = (
        "task_name",
        "executor__full_name",
    )
    list_filter = (
        "status",
        "deadline",
        "executor",
    )
    ordering = ("deadline",)
