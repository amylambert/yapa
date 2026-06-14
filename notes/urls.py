from django.urls import path
from .views import (
    NoteCreateView,
    NoteDetailView,
    NoteInlineUpdateView,
    NoteDeleteView,
)

urlpatterns = [
    path(
        "workspaces/<int:workspace_id>/notes/create/",
        NoteCreateView.as_view(),
        name="note-create",
    ),
    path(
        "notes/<int:pk>/",
        NoteDetailView.as_view(),
        name="note-detail",
    ),
    path(
        "notes/<int:pk>/inline-update/",
        NoteInlineUpdateView.as_view(),
        name="note-inline-update",
    ),
    path(
        "notes/<int:pk>/delete/",
        NoteDeleteView.as_view(),
        name="note-delete",
    ),
]