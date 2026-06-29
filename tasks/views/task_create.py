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

        # Context A: Task is built inside an explicit project container
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

        # Context B: Task is standalone but nested under a standalone note
        else:
            note_parent_id = self.request.GET.get("note_parent")
            if note_parent_id:
                form.instance.related_note = get_object_or_404(
                    Note, pk=note_parent_id, owner=self.request.user
                )

            parent_id = self.request.GET.get("parent")
            if parent_id:
                form.instance.parent = get_object_or_404(
                    Task, pk=parent_id, owner=self.request.user
                )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to structural parent asset contexts."""
        project_pk = self.kwargs.get("project_pk")
        note_parent_id = self.request.GET.get("note_parent")
        parent_id = self.request.GET.get("parent")

        # Project redirections
        if project_pk:
            if note_parent_id:
                return reverse(
                    "note-detail",
                    kwargs={"project_id": project_pk, "pk": note_parent_id},
                )
            if parent_id:
                return reverse(
                    "task-detail",
                    kwargs={"project_pk": project_pk, "pk": parent_id},
                )
            return reverse("project-detail", kwargs={"pk": project_pk})

        # Standalone redirections
        if note_parent_id:
            return reverse(
                "global-note-detail", 
                kwargs={"pk": note_parent_id}
            )
        if parent_id:
            return reverse(
                "global-task-detail",
                kwargs={"pk": parent_id}
            )

        return reverse("task-list")