from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from ..models import Project


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Controller to safely delete an existing project."""

    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("core:dashboard")

    def get_queryset(self):
        """Ensure users can only delete their own projects."""
        return Project.objects.filter(owner=self.request.user)