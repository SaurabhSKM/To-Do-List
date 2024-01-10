from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import TaskSerializer, TagSerializer
from .models import Task, Tag

# Create your views here.


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def AuthorizationView(request):
    msg = {
        "message": f"Hi {request.user.username}! Congratulations on being authenticated!"
    }
    return Response(msg, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def taskOverview(request):
    task_urls = {
        "List": "/task-list/",
        "Detail-View": "/task-detail/<str:pk>/",
        "Create": "/task-create/",
        "Delete": "/task-delete/<str:pk>/",
        "Update": "/task-update/<str:pk>/",
    }
    return Response(task_urls)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def taskCreate(request):
    # Extract data from the request
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


@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Task deleted successfully.")


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def tagList(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)
