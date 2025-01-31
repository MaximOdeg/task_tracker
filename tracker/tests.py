from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from users.models import Employee

from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        """Создаем тестового сотрудника и задачи для проверки"""
        self.employee = Employee.objects.create(
            full_name="Иван Иванов", position="Менеджер"
        )
        self.task1 = Task.objects.create(
            task_name="Задача 1",
            deadline=timezone.now().date() + timedelta(days=5),
        )
        self.task2 = Task.objects.create(
            task_name="Задача 2",
            parent_task=self.task1,  # Связываем задачу 2 с задачей 1
            deadline=timezone.now().date() + timedelta(days=10),
        )

    def test_task_creation(self):
        """Проверяем создание задачи"""
        self.assertEqual(self.task1.task_name, "Задача 1")
        self.assertEqual(self.task1.deadline, timezone.now().date() + timedelta(days=5))
        self.assertEqual(
            self.task1.status, "Not Started"
        )  # Проверка значения по умолчанию

    def test_task_parent_task(self):
        """Проверяем, что подзадача правильно связывается с родительской задачей"""
        self.assertEqual(
            self.task2.parent_task, self.task1
        )  # Проверяем, что родительская задача связана с подзадачей
        self.assertIn(
            self.task2, self.task1.subtasks.all()
        )  # Проверка, что задача 2 является подзадачей задачи 1

    def test_task_executor(self):
        """Проверяем, что исполнитель может быть правильно назначен на задачу"""
        self.task1.executor = self.employee
        self.task1.save()
        self.assertEqual(
            self.task1.executor, self.employee
        )  # Проверяем, что исполнитель назначен

    def test_task_status(self):
        """Проверяем, что статус задачи можно изменить"""
        self.task1.status = "In Progress"
        self.task1.save()
        self.assertEqual(
            self.task1.status, "In Progress"
        )  # Проверяем, что статус изменен

    def test_task_str_method(self):
        """Проверяем метод __str__"""
        self.assertEqual(
            str(self.task1), "Задача 1"
        )  # Проверяем, что метод __str__ возвращает правильное имя задачи
