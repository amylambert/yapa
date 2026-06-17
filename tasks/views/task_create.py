from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from workspaces.models import Workspace
from notes.models import Note
from ..models import Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure creation of tasks, sub-tasks, and note-tasks."""

    model = Task
    # Generate the form automatically using explicit model fields
    fields = ["title", "status", "deadline"]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        """Bind task to workspace, parent task, or parent note context."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        form.instance.workspace = workspace

        # Scenario A: Nested under another task
        parent_id = self.request.GET.get("parent")
        if parent_id:
            parent_task = get_object_or_404(
                Task, pk=parent_id, workspace=workspace
            )
            form.instance.parent = parent_task

        # Scenario B: Nested under a documentation note
        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            related_note = get_object_or_404(
                Note, pk=note_parent_id, workspace=workspace
            )
            form.instance.related_note = related_note

            # Inherit the deadline from the parent note if applicable
            if related_note.deadline and not form.instance.deadline:
                form.instance.deadline = related_note.deadline

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user back to the exact originating detail page."""
        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            return reverse("note-detail", kwargs={"pk": note_parent_id})

        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse(
                "task-detail",
                kwargs={
                    "workspace_id": self.kwargs["workspace_id"],
                    "pk": parent_id,
                },
            )

        return reverse(
            "workspace-detail",
            kwargs={"pk": self.kwargs["workspace_id"]},
        )