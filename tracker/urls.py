from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "employee/<int:employee_id>/",
        TaskViewSet.as_view({"get": "get_tasks_by_employee"}),
    ),
    path("important_tasks/", TaskViewSet.as_view({"get": "important_tasks", "post": "create_important_task"})),
]
