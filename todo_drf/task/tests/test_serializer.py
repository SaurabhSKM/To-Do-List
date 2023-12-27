from django.test import TestCase
from ..models import Tag, Task
from ..serializers import TagSerializer, TaskSerializer
import datetime


class TagSerializerTestCase(TestCase):
    def test_tag_serializer_valid_data(self):
        data = {"title": "Tag1"}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_tag_serializer_output(self):
        tag = Tag.objects.create(title="Tag1")
        serializer = TagSerializer(tag)
        expected_data = {"id": tag.id, "title": "Tag1"}
        self.assertEqual(serializer.data, expected_data)


class TaskSerializerTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(title="Tag1")
        self.tag2 = Tag.objects.create(title="Tag2")

    def test_task_serializer_valid_data(self):
        data = {
            "title": "Task1",
            "description": "Description1",
            "Due_date": "2024-01-12",  # Provide a valid date string
            "status": "OPEN",
            "tags": [self.tag1.id, self.tag2.id],
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_task_serializer_invalid_data(self):
        data = {
            "title": "",
            "description": "New Description",
            "Due_date": "2024-01-23",
            "status": "OPEN",
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_task_serializer_output(self):
        task = Task.objects.create(
            title="New Task",
            description="New Description",
            Due_date="2024-01-23",
            status="OPEN",
        )
        task.tag.add(self.tag1, self.tag2)
        serializer = TaskSerializer(task)
        expected_created_at = task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        expected_data = {
            "id": task.id,
            "title": "New Task",
            "description": "New Description",
            "Due_date": "2024-01-23",
            "created_at": expected_created_at,
            "status": "OPEN",
            "tag": [self.tag1.id, self.tag2.id],
        }
        self.assertEqual(serializer.data, expected_data)
