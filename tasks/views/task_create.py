from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from workspaces.models import Workspace
from ..models import Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Controller handling the creation of workspace-linked tasks."""

    model = Task
    fields = ["title", "description", "status", "priority", "due_date"]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        """Bind the task to the parent workspace container securely."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_pk"],
            owner=self.request.user,
        )
        form.instance.workspace = workspace
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the parent workspace dashboard view."""
        return reverse(
            "workspace-detail",
            kwargs={"pk": self.kwargs["workspace_pk"]},
        )