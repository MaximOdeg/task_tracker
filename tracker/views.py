from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Employee, Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций с задачами"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=["get"], url_path="employee/(?P<employee_id>\\d+)")
    def get_tasks_by_employee(self, request, employee_id=None):
        """Получить задачи для конкретного сотрудника"""
        tasks = Task.objects.filter(executor__id=employee_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def important_tasks(self, request):
        """Получение важных задач"""
        important_tasks = Task.objects.filter(
            executor__isnull=True, parent_task__isnull=False
        )

        result = []
        for task in important_tasks:
            executors = Employee.objects.filter(tasks__parent_task=task).annotate(
                task_count=Count("tasks")
            )
            # Сортируем по количеству задач и выбираем наименее загруженного сотрудника
            executors = executors.order_by("task_count")[:1]
            result.append(
                {
                    "task_name": task.task_name,
                    "deadline": task.deadline,
                    "executors": [employee.full_name for employee in executors],
                }
            )

        return Response(result)
