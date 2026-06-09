from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from ..models import Workspace


class WorkspaceDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Controller to safely delete an existing workspace."""

    model = Workspace
    template_name = "workspaces/workspace_confirm_delete.html"
    success_url = reverse_lazy("workspace-list")

    def get_queryset(self):
        """Ensure users can only delete their own workspaces."""
        return Workspace.objects.filter(owner=self.request.user)