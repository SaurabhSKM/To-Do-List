# tasks/tests/test_views.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Task, Tag


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
        # Define valid data for the task
        valid_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "Due_date": "2024-01-12",
            "status": "OPEN",
            "tag": ["tag1", "tag2"],
        }

        # Make a POST request to the taskCreate endpoint with valid data
        self.client.post("/task-create/", valid_data, format="json")

        # Assert that a task with the given title exists in the database
        created_task = Task.objects.get(title="Test Task")
        self.assertIsNotNone(created_task)

        # Optionally, you can add more assertions based on your specific requirements
        # For example, you might want to check if the tags are associated with the task.

        # Example assertion to check if the tags are associated with the task
        self.assertEqual(
            list(created_task.tag.values_list("title", flat=True)), ["tag1", "tag2"]
        )

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
            "tag": ["tag1", "tag2"],
        }
        response = self.client.post(f"/task-update/{task.id}/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Task")
        self.assertEqual(response.data["description"], "Updated Description")
        self.assertEqual(response.data["Due_date"], "2024-01-12")
        self.assertEqual(response.data["status"], "OPEN")
        self.assertEqual(response.data["tag"], ["tag1", "tag2"])

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
        Tag.objects.create(id="Tag1", title="Tag1")
        Tag.objects.create(id="Tag2", title="Tag2")

        response = self.client.get("/tag-list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Assuming there are 2 tags in the database

    def test_task_update_invalid_data(self):
        # Define invalid data (modify this based on your serializer validation requirements)
        task = Task.objects.create(
            title="Task1",
            description="Description1",
            Due_date="2024-01-12",
            status="OPEN",
        )
        invalid_data = {
            "title": "",
            "description": "",
            "Due_date": "invalid_date",
            "status": "INVALID_STATUS",
        }

        # Make a POST request to the taskCreate endpoint with invalid data
        response = self.client.post(
            f"/task-update/{task.id}/", invalid_data, format="json"
        )

        # Assert that the response status code is 200 (or the appropriate status code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected message for invalid data
        self.assertEqual(response.data, "Data is invalid")

    def test_task_create_invalid_data(self):
        # Define invalid data (modify this based on your serializer validation requirements)
        invalid_data = {
            "title": "",
            "description": "",
            "Due_date": "invalid_date",
            "status": "INVALID_STATUS",
        }

        # Make a POST request to the taskCreate endpoint with invalid data
        response = self.client.post("/task-create/", invalid_data, format="json")

        # Assert that the response status code is 200 (or the appropriate status code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected message for invalid data
        self.assertEqual(response.data, "Data is invalid")

        # Example assertion to check if the number of tasks in the database is not increased
        self.assertEqual(Task.objects.count(), 0)
