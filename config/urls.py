# config/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

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
]