from django.urls import path
from .views import TaskCreateView

urlpatterns = [
    path(
        "workspaces/<int:workspace_pk>/tasks/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
]