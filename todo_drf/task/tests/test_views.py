# tasks/tests/test_views.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Task, Tag
from ..serializers import TaskSerializer, TagSerializer


class TaskViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authorization_view(self):
        response = self.client.get("/auth/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            f"Hi {self.user.username}! Congratulations on being authenticated!",
        )

    def test_task_overview(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("List", response.data)
        self.assertIn("Detail-View", response.data)
        self.assertIn("Create", response.data)
        self.assertIn("Delete", response.data)
        self.assertIn("Update", response.data)

    def test_task_list(self):
        # Create some tasks for testing
        Task.objects.create(
            title="Task1",
            description="Description1",
            Due_date="2024-01-12",
            status="OPEN",
        )
        Task.objects.create(
            title="Task2",
            description="Description2",
            Due_date="2024-01-22",
            status="OPEN",
        )
        response = self.client.get("/task-list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Assuming there are 2 tasks in the database

    def test_task_detail(self):
        task = Task.objects.create(
            title="Task1",
            description="Description1",
            Due_date="2024-01-12",
            status="OPEN",
        )
        response = self.client.get(f"/task-detail/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Task1")
        self.assertEqual(response.data["description"], "Description1")
        self.assertEqual(response.data["Due_date"], "2024-01-12")
        self.assertEqual(response.data["status"], "OPEN")

    def test_task_create(self):
        data = {
            "title": "New Task",
            "description": "New Description",
            "Due_date": "2024-01-23",
            "status": "OPEN",
        }
        response = self.client.post("/task-create/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["description"], "New Description")
        self.assertEqual(response.data["Due_date"], "2024-01-23")
        self.assertEqual(response.data["status"], "OPEN")

    def test_task_update(self):
        task = Task.objects.create(
            title="Task1",
            description="Description1",
            Due_date="2024-01-12",
            status="OPEN",
        )
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "Due_date": "2024-01-12",
            "status": "OPEN",
        }
        response = self.client.post(f"/task-update/{task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task")
        self.assertEqual(response.data["description"], "Updated Description")
        self.assertEqual(response.data["Due_date"], "2024-01-12")
        self.assertEqual(response.data["status"], "OPEN")

    def test_task_delete(self):
        task = Task.objects.create(
            title="Task1",
            description="Description1",
            Due_date="2024-01-12",
            status="OPEN",
        )
        response = self.client.delete(f"/task-delete/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Task deleted successfully.")

    def test_tag_list(self):
        # Create some tags for testing
        Tag.objects.create(title="Tag1")
        Tag.objects.create(title="Tag2")

        response = self.client.get("/tag-list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Assuming there are 2 tags in the database
