from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Controller handling the centralized view of an isolated task."""

    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        """Ensure users can only view tasks inside their owned workspaces."""
        return Task.objects.filter(workspace__owner=self.request.user)

    def get_context_data(self, **kwargs):
        """Inject sub-tasks and separate them from parent-level nodes."""
        context = super().get_context_data(**kwargs)
        # Fetch pre-related subtasks using our model related_name
        context["subtasks"] = self.object.subtasks.all()
        return context