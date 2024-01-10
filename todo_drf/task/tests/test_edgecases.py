from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from ..models import Task, Tag


class TaskEdgeCases(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(id="Tag1", title="Tag1")
        self.tag2 = Tag.objects.create(id="Tag2", title="Tag2")

    def test_create_task_with_empty_title(self):
        with self.assertRaises(ValidationError):
            task = Task(title="", description="Description", Due_date=date.today())
            task.full_clean()

    def test_create_task_with_long_description(self):
        # Create a description longer than the allowed max_length
        long_description = "A" * 1001
        with self.assertRaises(ValidationError):
            task = Task(
                title="Title", description=long_description, Due_date=date.today()
            )
            task.full_clean()

    def test_create_task_with_past_due_date(self):
        # Create a task with a due date in the past
        past_due_date = date.today() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            task = Task(
                title="Title", description="Description", Due_date=past_due_date
            )
            task.full_clean()

    def test_create_task_with_tags(self):
        # Create a task with associated tags
        task = Task(title="Title", description="Description", Due_date=date.today())
        task.save()
        task.tag.add(self.tag1, self.tag2)
        self.assertEqual(task.tag.count(), 2)

    def test_create_task_with_invalid_status_choice(self):
        # Try to create a task with an invalid status choice
        with self.assertRaises(ValidationError):
            task = Task(
                title="Title",
                description="Description",
                Due_date=date.today(),
                status="INVALID_STATUS",
            )
            task.full_clean()


class TagEdgeCase(TestCase):
    def test_create_tag_with_empty_title_and_id(self):
        with self.assertRaises(ValidationError):
            tag = Tag(id="", title="")
            tag.full_clean()

    def test_create_tag_with_long_title_and_id(self):
        # Create a title longer than the allowed max_length
        long_title = "A" * 51
        with self.assertRaises(ValidationError):
            tag = Tag(id=long_title, title=long_title)
            tag.full_clean()

    def test_create_tag_with_valid_data(self):
        # Create a tag with valid data
        tag = Tag(id="ValidID", title="ValidTitle")
        tag.full_clean()  # This should not raise a ValidationError

    def test_create_tag_with_duplicate_title_and_id(self):
        # Create a tag with a duplicate title
        tag1 = Tag(id="ValidID", title="DuplicateTitle")
        tag1.save()

        # Try to create another tag with the same title
        with self.assertRaises(ValidationError):
            tag2 = Tag(id="ValidID", title="DuplicateTitle")
            tag2.full_clean()
