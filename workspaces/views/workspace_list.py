from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Workspace


class WorkspaceListView(LoginRequiredMixin, generic.ListView):
    """Controller displaying workspaces for the logged-in user."""

    model = Workspace
    template_name = "workspaces/workspace_list.html"
    context_object_name = "workspaces"

    def get_queryset(self):
        """Filter workspaces to ensure privacy boundary execution."""
        return Workspace.objects.filter(owner=self.request.user)