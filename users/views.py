from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций с сотрудниками"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=["get"], url_path="employees")
    def list_employees(self, request, *args, **kwargs):
        """Получение списка всех сотрудников"""
        employees = self.queryset

        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Получение списка сотрудников, отсортированных по количеству активных задач"""

        employees = (
            Employee.objects.annotate(
                active_tasks_count=Count("tasks", filter=Q(tasks__status="In Progress"))
            )
            .prefetch_related("tasks")
            .order_by("-active_tasks_count")
        )

        result = []
        for employee in employees:
            result.append(
                {
                    "full_name": employee.full_name,
                    "active_tasks_count": employee.active_tasks_count,
                    "tasks": [
                        {"task_name": task.task_name, "status": task.status}
                        for task in employee.tasks.all()
                    ],
                }
            )

        return Response(result)
