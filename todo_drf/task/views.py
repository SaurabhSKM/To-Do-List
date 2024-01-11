from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import TaskSerializer, TagSerializer
from .models import Task, Tag


class AuthorizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        msg = {
            "message": f"Hi {request.user.username}! Congratulations on being authenticated!"
        }
        return Response(msg, status=status.HTTP_200_OK)


class TaskOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_urls = {
            "List": "/task-list/",
            "Detail-View": "/task-detail/<str:pk>/",
            "Create": "/task-create/",
            "Delete": "/task-delete/<str:pk>/",
            "Update": "/task-update/<str:pk>/",
        }
        return Response(task_urls)


class TaskList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tasks = Task.objects.get(id=pk)
        serializer = TaskSerializer(tasks, many=False)
        return Response(serializer.data)


class TaskUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        title = request.data.get("title")
        description = request.data.get("description")
        due_date = request.data.get("Due_date")
        status = request.data.get("status")
        tag_titles = request.data.get("tag", [])

        # Check if the tags exist, create them if not present
        tags = []
        for tag_title in tag_titles:
            tag, created = Tag.objects.get_or_create(
                title=tag_title, defaults={"id": tag_title}
            )
            tags.append(tag)

        # Create a new task with the extracted data and tags
        task_data = {
            "title": title,
            "description": description,
            "Due_date": due_date,
            "status": status,
        }

        # Adding tags to the task data
        task_data["tag"] = tags

        serializer = TaskSerializer(instance=task, data=task_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("Data is invalid")


class TaskCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        due_date = request.data.get("Due_date")
        status = request.data.get("status")
        tag_titles = request.data.get("tag", [])

        # Check if the tags exist, create them if not present
        tags = []
        for tag_title in tag_titles:
            tag, created = Tag.objects.get_or_create(
                title=tag_title, defaults={"id": tag_title}
            )
            tags.append(tag)

        # Create a new task with the extracted data and tags
        task_data = {
            "title": title,
            "description": description,
            "Due_date": due_date,
            "status": status,
        }

        # Adding tags to the task data
        task_data["tag"] = tags

        serializer = TaskSerializer(data=task_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("Data is invalid")


class TaskDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.delete()
        return Response("Task deleted successfully.")


class TagList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
