from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Project


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    """Renders the operations panel for a single project engine."""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        """Return the user's project optimized for related components."""
        return (
            Project.objects.filter(owner=self.request.user)
            .prefetch_related("tasks", "notes")
        )