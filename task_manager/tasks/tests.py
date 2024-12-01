from django.test import TestCase
from .models import Task

class TaskManagerTests(TestCase):
    def setUp(self):

        self.task = Task.objects.create(
            title="Тестовая задача",
            description="Описание тестовой задачи",
            category="Тест",
            due_date="2024-12-31",
            priority=Task.MEDIUM,
        )

    def test_task_creation(self):

        self.assertEqual(self.task.title, "Тестовая задача")
        self.assertEqual(self.task.status, Task.NOT_DONE)
        self.assertEqual(self.task.due_date, "2024-12-31")

    def test_task_update(self):

        self.task.status = Task.DONE
        self.task.save()
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.status, Task.DONE)

    def test_task_deletion(self):

        task_id = self.task.id
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_task_search(self):

        tasks = Task.objects.filter(title__icontains="Тестовая")
        self.assertTrue(tasks.exists())

    def test_switch_status(self):

        self.task.switch_status()
        self.assertEqual(self.task.status, Task.DONE)

        self.task.switch_status()
        self.assertEqual(self.task.status, Task.NOT_DONE)
