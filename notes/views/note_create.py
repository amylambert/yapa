from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from workspaces.models import Workspace
from ..models import Note
from ..forms import NoteForm


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure, contextual composition of notes inside a workspace."""

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"

    def form_valid(self, form):
        """Bind the note to the parent workspace after ownership validation."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        form.instance.workspace = workspace
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the author back to the parent workspace workspace."""
        return reverse(
            "workspace-detail",
            kwargs={"pk": self.kwargs["workspace_id"]},
        )