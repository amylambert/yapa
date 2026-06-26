from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectInlineUpdateView,
)
# Import your master dashboard view here
# from dashboard.views import DashboardView 

urlpatterns = [
    # Re-route the old list view directly to the dashboard view instead
    # path("projects/", DashboardView.as_view(), name="project-list"),
    
    path(
        "projects/create/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
        "projects/<int:pk>/inline-update/",
        ProjectInlineUpdateView.as_view(),
        name="project-inline-update",
    ),
]