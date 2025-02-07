from rest_framework import serializers

from users.models import Employee

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False, allow_null=True
    )
    executor = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = ["id", "task_name", "parent_task", "executor", "deadline", "status"]
