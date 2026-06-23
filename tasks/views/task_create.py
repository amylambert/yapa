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
    # Whitelist form fields explicitly to avoid model layer exposure
    fields = ["title", "status", "deadline", "priority", "description"]
    template_name = "tasks/task_form.html"

    def _get_workspace_id(self) -> int:
        """Extract workspace identifier from URL arguments safely."""
        return (
            self.kwargs.get("workspace_pk")
            or self.kwargs.get("workspace_id")
            or self.kwargs.get("pk")
        )

    def form_valid(self, form):
        """Bind task to workspace, parent task, or parent note context."""
        workspace_id = self._get_workspace_id()
        workspace = get_object_or_404(
            Workspace,
            pk=workspace_id,
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

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user back to the exact originating detail page."""
        workspace_id = self._get_workspace_id()
        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            return reverse("note-detail", kwargs={"pk": note_parent_id})

        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse(
                "task-detail",
                kwargs={
                    "workspace_pk": workspace_id,
                    "pk": parent_id,
                },
            )

        return reverse(
            "workspace-detail",
            kwargs={"pk": workspace_id},
        )