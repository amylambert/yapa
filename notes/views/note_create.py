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

    def post(self, request, *args, **kwargs):
        """Bind relationships before form validation executes."""
        self.object = None
        form = self.get_form()

        # Resolve and bind workspace before validation checks run
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_id"],
            owner=request.user,
        )
        form.instance.workspace = workspace

        # Resolve and bind parent note hierarchy if present
        parent_id = request.GET.get("parent")
        if parent_id:
            form.instance.parent = get_object_or_404(
                Note, pk=parent_id, workspace=workspace
            )

        # Resolve and bind related task anchor if present
        task_parent_id = request.GET.get("task_parent")
        if task_parent_id:
            form.instance.related_task = get_object_or_404(
                Task, pk=task_parent_id, workspace=workspace
            )

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """Save the securely pre-populated model instance."""
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the author back to the exact originating detail page."""
        task_parent_id = self.request.GET.get("task_parent")
        if task_parent_id:
            return reverse(
                "task-detail",
                kwargs={
                    "workspace_pk": self.kwargs["workspace_id"],
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