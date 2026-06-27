from django.urls import path
from . import views

urlpatterns = [
    path(
        "projects/<int:project_id>/notes/create/",
        views.NoteCreateView.as_view(),
        name="note-create",
    ),
    path(
        "projects/<int:project_id>/notes/<int:pk>/",
        views.NoteDetailView.as_view(),
        name="note-detail",
    ),
    path(
        "projects/<int:project_id>/notes/<int:pk>/inline-update/",
        views.NoteInlineUpdateView.as_view(),
        name="note-inline-update",
    ),
    path(
        "projects/<int:project_id>/notes/<int:pk>/delete/",
        views.NoteDeleteView.as_view(),
        name="note-delete",
    ),
]