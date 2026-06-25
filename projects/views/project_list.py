from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Project


class ProjectListView(LoginRequiredMixin, generic.ListView):
    """Controller displaying active projects for the main view frame."""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)