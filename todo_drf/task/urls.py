from django.urls import  path
from . import views

urlpatterns=[
    path('',views.taskOverview , name="task-overview"),
    path('auth/', views.AuthorizationView,name="AuthorizationView"),
    path('task-list/', views.taskList, name="task-list"),
    path('task-detail/<str:pk>/',views.taskDetail,name="task-detail"),
    path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('task-create/', views.taskCreate, name="task-create"),
    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
     path('tag-list/', views.tagList, name="tag-list"),
]