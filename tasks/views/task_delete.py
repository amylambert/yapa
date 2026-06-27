from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from ..models import Task


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Controller to safely delete an existing task or sub-task."""

    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_queryset(self):
        """Ensure users can only delete tasks within owned spaces."""
        return Task.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        """Redirect back to project detail page after deletion."""
        return reverse(
            "project-detail",
            kwargs={"pk": self.kwargs["project_pk"]},
        )