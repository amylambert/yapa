from django.urls import path
from .views import WorkspaceCreateView, WorkspaceListView

urlpatterns = [
    path(
        "workspaces/",
        WorkspaceListView.as_view(),
        name="workspace-list",
    ),
    path(
        "workspaces/create/",
        WorkspaceCreateView.as_view(),
        name="workspace-create",
    ),
]