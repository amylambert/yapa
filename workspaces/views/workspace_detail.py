from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Workspace


class WorkspaceDetailView(LoginRequiredMixin, generic.DetailView):
    """Renders the comprehensive operations dashboard for a single workspace."""

    model = Workspace
    template_name = "workspaces/workspace_detail.html"
    context_object_name = "workspace"

    def get_queryset(self):
        """Return the user's workspace optimized for related components."""
        return (
            Workspace.objects.filter(owner=self.request.user)
            .prefetch_related("tasks", "notes")
        )