# config/urls.py
from django.urls import include, path
from django.views.generic import RedirectView
from notes.views import NoteCreateView
from tasks.views import TaskCreateView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="core:dashboard",
            permanent=False,
        ),
    ),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),    
    path("", include("projects.urls")),
    path("", include("tasks.urls")),
    path("", include("notes.urls")),
    path(
        "tasks/create/", 
        TaskCreateView.as_view(), 
        name="global-task-create"
    ),
    path(
        "notes/create/", 
        NoteCreateView.as_view(), 
        name="global-note-create"
    ),
]