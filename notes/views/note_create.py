from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from workspaces.models import Workspace
from ..models import Note
from ..forms import NoteForm


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure creation of root notes and nested sub-notes."""

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        """Bind note to workspace and optional parent via query string."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        form.instance.workspace = workspace

        # Extract parent pointer out of incoming GET stream params
        parent_id = self.request.GET.get("parent")
        if parent_id:
            parent_note = get_object_or_404(
                Note,
                pk=parent_id,
                workspace=workspace,
            )
            form.instance.parent = parent_note

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the author back to the contextual detail dashboard."""
        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse("note-detail", kwargs={"pk": parent_id})
        return reverse(
            "workspace-detail",
            kwargs={"pk": self.kwargs["workspace_id"]},
        )