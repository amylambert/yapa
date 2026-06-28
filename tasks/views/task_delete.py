from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views import generic
from ..models import Task


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Controller to safely delete an existing task or sub-task."""

    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_queryset(self):
        """Ensure users can only delete spaces they own."""
        return Task.objects.filter(
            Q(owner=self.request.user) |
            Q(project__owner=self.request.user)
        ).distinct()

    def get_success_url(self):
        """Redirect back to project detail page or global list."""
        if self.object.project:
            return reverse(
                "project-detail",
                kwargs={"pk": self.object.project.pk},
            )
        return reverse("task-list")