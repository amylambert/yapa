from django.urls import path
from .views import (
    WorkspaceCreateView,
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceUpdateView,
    WorkspaceDeleteView,
)

urlpatterns = [
    # Workspace list, create, and detail views
    path(
        "workspaces/",
        WorkspaceListView.as_view(),
        name="workspace-list",
    ),
    # Workspace creation page
    path(
        "workspaces/create/",
        WorkspaceCreateView.as_view(),
        name="workspace-create",
    ),
    # Workspace detail page
    path(
        "workspaces/<int:pk>/",
        WorkspaceDetailView.as_view(),
        name="workspace-detail",
    ),
    # Workspace update page
    path(
        "workspaces/<int:pk>/update/",
        WorkspaceUpdateView.as_view(),
        name="workspace-update",
    ),
    # Workspace delete page
    path(
        "workspaces/<int:pk>/delete/",
        WorkspaceDeleteView.as_view(),
        name="workspace-delete",
    ),
]