from django.urls import path
from .views import NoteCreateView

urlpatterns = [
    path(
        "workspaces/<int:workspace_id>/notes/create/",
        NoteCreateView.as_view(),
        name="note-create",
    ),
]