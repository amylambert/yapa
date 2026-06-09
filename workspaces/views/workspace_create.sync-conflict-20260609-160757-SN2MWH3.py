from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from ..models import Workspace


class WorkspaceCreateView(LoginRequiredMixin, generic.CreateView):
    """Controller for creating a new workspace under the current user."""

    model = Workspace
    fields = ["name", "description"]
    template_name = "workspaces/workspace_form.html"
    success_url = reverse_lazy("workspace-list")

    def form_valid(self, form):
        """Automatically assign the logged-in user as the owner."""
        form.instance.owner = self.request.user
        return super().form_valid(form)