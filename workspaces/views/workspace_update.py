from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from ..models import Workspace


class WorkspaceUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Controller to edit an existing workspace configuration."""

    model = Workspace
    fields = ["name", "description"]
    template_name = "workspaces/workspace_form.html"

    def get_queryset(self):
        """Ensure users can only edit their own workspaces."""
        return Workspace.objects.filter(owner=self.request.user)

    def get_success_url(self):
        """Redirect dynamically to the updated workspace's detail page."""
        return reverse("workspace-detail", kwargs={"pk": self.object.pk})