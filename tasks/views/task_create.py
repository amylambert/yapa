from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from notes.models import Note
from projects.models import Project
from ..models import Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure generation of tasks nested or standalone."""

    model = Task
    fields = [
        "name",
        "status",
        "start_date",
        "end_date",
        "priority",
        "description",
        "time_estimate",
    ]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        """Bind task to its structural layers or owner context."""
        project_id = self.kwargs.get("project_pk")
        form.instance.owner = self.request.user

        # Safely capture project mapping chains only if parameters exist
        if project_id:
            project_instance = get_object_or_404(
                Project,
                pk=project_id,
                owner=self.request.user,
            )
            form.instance.project = project_instance

            parent_id = self.request.GET.get("parent")
            if parent_id:
                form.instance.parent = get_object_or_404(
                    Task, pk=parent_id, project=project_instance
                )

            note_parent_id = self.request.GET.get("note_parent")
            if note_parent_id:
                form.instance.related_note = get_object_or_404(
                    Note, pk=note_parent_id, project=project_instance
                )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user back to the correct context page."""
        project_id = self.kwargs.get("project_pk")
        if not project_id:
            return reverse("core:dashboard")

        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            return reverse("note-detail", kwargs={"pk": note_parent_id})

        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse(
                "task-detail",
                kwargs={"project_pk": project_id, "pk": parent_id},
            )

        return reverse("project-detail", kwargs={"pk": project_id})