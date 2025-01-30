from django.test import TestCase

from .models import Employee


class EmployeeModelTest(TestCase):
    def setUp(self):
        """Создаем тестового сотрудника"""
        self.employee = Employee.objects.create(
            full_name="Иван Иванов", position="Менеджер"
        )

    def test_employee_creation(self):
        """Проверяем, что сотрудник был успешно создан"""
        self.assertEqual(self.employee.full_name, "Петр Иванов")
        self.assertEqual(self.employee.position, "Менеджер")

    def test_employee_str_method(self):
        """Проверяем метод __str__"""
        self.assertEqual(str(self.employee), "Петр Иванов")

    def test_employee_position(self):
        """Проверяем, что поле должности верно хранится"""
        self.assertEqual(self.employee.position, "Менеджер")
