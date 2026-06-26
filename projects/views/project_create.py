from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from ..models import Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    """Controller for creating a new project under the current user."""

    model = Project
    fields = ["name", "description", "priority", "start_date", "end_date"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        """Automatically assign the logged-in user as the owner."""
        form.instance.owner = self.request.user
        return super().form_valid(form)