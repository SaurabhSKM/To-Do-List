# tasks/tests/test_models.py

from django.test import TestCase
from ..models import Task, Tag
from datetime import date


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(title="Tag1")
        self.tag2 = Tag.objects.create(title="Tag2")

    def test_create_task_with_valid_data(self):
        task = Task.objects.create(
            title="Valid Task",
            description="Valid description",
            Due_date=date.today(),
            status="OPEN",
        )
        task.tag.add(self.tag1, self.tag2)

        self.assertEqual(task.title, "Valid Task")
        self.assertEqual(task.description, "Valid description")
        self.assertEqual(task.Due_date, date.today())
        self.assertEqual(task.status, "OPEN")
        self.assertEqual(task.tag.count(), 2)

    def test_update_task(self):
        task = Task.objects.create(
            title="Original Task",
            description="Original description",
            Due_date=date.today(),
            status="OPEN",
        )

        task.title = "Updated Task"
        task.description = "Updated description"
        task.Due_date = date.today()
        task.status = "WORKING"
        task.save()

        updated_task = Task.objects.get(id=task.id)

        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated description")
        self.assertEqual(updated_task.Due_date, date.today())
        self.assertEqual(updated_task.status, "WORKING")

    def test_delete_task(self):
        task = Task.objects.create(
            title="Task to Delete",
            description="Description to delete",
            Due_date=date.today(),
            status="OPEN",
        )
        task_id = task.id
        task.delete()

        with self.assertRaises(Task.DoesNotExist):
            # Attempt to retrieve the deleted task should raise a DoesNotExist exception
            Task.objects.get(id=task_id)

    def test_str_method_returns_title(self):
        # Create a Task instance
        task = Task.objects.create(
            title="Valid Task",
            description="Valid description",
            Due_date=date.today(),
            status="OPEN",
        )
        task.tag.add(self.tag1)
        # Check that the __str__ method returns the title
        self.assertEqual(str(task), "Valid Task")
