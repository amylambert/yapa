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
]