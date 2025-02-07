from django.db import models


class Employee(models.Model):
    """ "Модель сотрудника"""

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Должность")

    def __str__(self):
        return f"{self.full_name} {self.position}"
