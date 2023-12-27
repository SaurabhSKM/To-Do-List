from django.test import TestCase

# Create your tests here.
from .test_models import TaskModelTestCase
from .test_serializer import TagSerializerTestCase,TaskSerializerTestCase
from .test_views import TaskViewsTestCase
from .test_edgecases import TaskEdgeCases,TagEdgeCase

__all__ = [
    'TaskModelTestCase',
    'TagSerializerTestCase',
    'TaskSerializerTestCase',
    'TaskViewsTestCase',
    'TaskEdgeCases',
    'TagEdgeCase'
    # Add other test classes if needed
]