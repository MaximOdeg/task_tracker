from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций с сотрудниками"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        """Получение списка сотрудников, отсортированных по количеству активных задач"""

        employees = Employee.objects.annotate(
            active_tasks_count=Count("tasks", filter=Q(tasks__is_active=True))
        ).order_by("-active_tasks_count")

        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)
