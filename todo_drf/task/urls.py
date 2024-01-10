from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskOverview.as_view(), name="task-overview"),
    path("auth/", views.AuthorizationView.as_view(), name="AuthorizationView"),
    path("task-list/", views.TaskList.as_view(), name="task-list"),
    path("task-detail/<str:pk>/", views.TaskDetail.as_view(), name="task-detail"),
    path("task-update/<str:pk>/", views.TaskUpdate.as_view(), name="task-update"),
    path("task-create/", views.TaskCreate.as_view(), name="task-create"),
    path("task-delete/<str:pk>/", views.TaskDelete.as_view(), name="task-delete"),
    path("tag-list/", views.TagList.as_view(), name="tag-list"),
]
