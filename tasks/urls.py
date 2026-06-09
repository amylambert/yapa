from django.urls import path
from . import views

urlpatterns = [
    # Task creation
    path(
        "workspaces/<int:workspace_pk>/tasks/new/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    # Task detail view
    path(
        "workspaces/<int:workspace_pk>/tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    # Sub-task creation linked to parent task
    path(
        "workspaces/<int:workspace_pk>/tasks/<int:parent_pk>/subtasks/new/",
        views.SubTaskCreateView.as_view(),
        name="subtask-create",
    ),
    # Inline asynchronous partial task updates
    path(
        "workspaces/<int:workspace_pk>/tasks/<int:pk>/update/",
        views.TaskInlineUpdateView.as_view(),
        name="task-inline-update",
    ),
]