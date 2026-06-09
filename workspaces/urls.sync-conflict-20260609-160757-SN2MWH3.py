from django.urls import path
from .views import (
    WorkspaceCreateView,
    WorkspaceDeleteView,
    WorkspaceDetailView,
    WorkspaceListView,
    WorkspaceUpdateView,
)

urlpatterns = [
    # workspace list
    path(
        "workspaces/",
        WorkspaceListView.as_view(),
        name="workspace-list",
    ),

    # workspace CRUD
    path(
        "workspaces/create/",
        WorkspaceCreateView.as_view(),
        name="workspace-create",
    ),
    path(
        "workspaces/<int:pk>/",
        WorkspaceDetailView.as_view(),
        name="workspace-detail",
    ),
    path(
        "workspaces/<int:pk>/edit/",
        WorkspaceUpdateView.as_view(),
        name="workspace-edit",
    ),
    path(
        "workspaces/<int:pk>/delete/",
        WorkspaceDeleteView.as_view(),
        name="workspace-delete",
    ),
]