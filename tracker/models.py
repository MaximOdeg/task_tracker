from django.db import models

from users.models import Employee


class Task(models.Model):
    """ "Модель задачи"""

    task_name = models.CharField(max_length=255, verbose_name="Задача")
    parent_task = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Родительская задача",
    )
    executor = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name="Исполнитель",
    )
    deadline = models.DateField(verbose_name="Срок выполнения")
    status = models.CharField(
        max_length=50,
        choices=[
            ("Not Started", "Не начата"),
            ("In Progress", "В процессе"),
            ("Completed", "Завершена"),
        ],
        default="Not Started",
        verbose_name="Статус",
    )

    def __str__(self):
        return self.task_name
