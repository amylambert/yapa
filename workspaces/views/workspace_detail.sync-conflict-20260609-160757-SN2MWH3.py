from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Workspace


class WorkspaceDetailView(LoginRequiredMixin, generic.DetailView):
    """Controller to display a workspace and its associated tasks."""

    model = Workspace
    template_name = "workspaces/workspace_detail.html"
    context_object_name = "workspace"

    def get_queryset(self):
        """Ensure users can only access their own workspaces."""
        return Workspace.objects.filter(owner=self.request.user)