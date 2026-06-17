from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from workspaces.models import Workspace
from tasks.models import Task
from ..models import Note
from ..forms import NoteForm


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure creation of root notes, sub-notes, and task-notes."""

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        """Bind note to workspace, parent note, or parent task context."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        form.instance.workspace = workspace

        # Scenario A: Nested under another note
        parent_id = self.request.GET.get("parent")
        if parent_id:
            parent_note = get_object_or_404(
                Note, pk=parent_id, workspace=workspace
            )
            form.instance.parent = parent_note

        # Scenario B: Nested under a task element
        task_parent_id = self.request.GET.get("task_parent")
        if task_parent_id:
            related_task = get_object_or_404(
                Task, pk=task_parent_id, workspace=workspace
            )
            form.instance.related_task = related_task

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the author back to the exact originating detail page."""
        task_parent_id = self.request.GET.get("task_parent")
        if task_parent_id:
            return reverse(
                "task-detail",
                kwargs={
                    "workspace_id": self.kwargs["workspace_id"],
                    "pk": task_parent_id,
                },
            )

        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse("note-detail", kwargs={"pk": parent_id})

        return reverse(
            "workspace-detail",
            kwargs={"pk": self.kwargs["workspace_id"]},
        )