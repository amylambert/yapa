from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from ..models import Task


class SubTaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Controller handling the creation of nested sub-tasks."""

    model = Task
    fields = ["title"]

    def form_valid(self, form):
        """Bind the sub-task to its parent task and workspace securely."""
        parent_task = get_object_or_404(
            Task,
            pk=self.kwargs["parent_pk"],
            workspace__owner=self.request.user,
        )
        form.instance.parent = parent_task
        form.instance.workspace = parent_task.workspace
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the parent task detail view dashboard."""
        return reverse(
            "task-detail",
            kwargs={
                "workspace_pk": self.kwargs["workspace_pk"],
                "pk": self.kwargs["parent_pk"],
            },
        )