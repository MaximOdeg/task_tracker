import logging

from celery import shared_task
from django.utils import timezone

from .models import Task

logger = logging.getLogger(__name__)


@shared_task
def send_task_deadline_reminder():
    """Напоминаем о задачах, у которых срок выполнения через 1 день"""
    tomorrow = (timezone.now() + timezone.timedelta(days=1)).date()
    tasks_due_tomorrow = Task.objects.filter(deadline=tomorrow, status="Not Started")

    for task in tasks_due_tomorrow:
        logger.info(
            f"Напоминаем о задаче: {task.task_name}, срок выполнения: {task.deadline}"
        )

    return f"Reminded about {len(tasks_due_tomorrow)} tasks."
