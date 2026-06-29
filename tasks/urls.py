from django.urls import path
from . import views

urlpatterns = [
    # Universal Task / Sub-Task Creation Entrypoint
    path(
        "projects/<int:project_pk>/tasks/new/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    # Central Task Detail Dashboard Interface
    path(
        "projects/<int:project_pk>/tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    # Asynchronous Partial Updates Interface Hook
    path(
        "projects/<int:project_pk>/tasks/<int:pk>/update/",
        views.TaskInlineUpdateView.as_view(),
        name="task-inline-update",
    ),
    # Permanent destruction confirmation of tasks
    path(
        "projects/<int:project_pk>/tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="global-task-detail",
    ),
    # Global Asynchronous Partial Updates Interface Hook
    path(
        "tasks/<int:pk>/update/",
        views.TaskInlineUpdateView.as_view(),
        name="global-task-inline-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="global-task-delete",
    ),
]