from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic
from ..models import Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Controller handling the centralized view of an isolated task."""

    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        """Ensure users can view tasks they own or inside owned projects."""
        return Task.objects.filter(
            Q(owner=self.request.user) | Q(project__owner=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        """Inject sub-tasks and separate them from parent-level nodes."""
        context = super().get_context_data(**kwargs)
        context["subtasks"] = self.object.subtasks.all()

        # Use the reverse relationship manager to query linked notes cleanly
        context["subnotes"] = self.object.linked_notes.all()
        return context