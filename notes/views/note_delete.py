from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from ..models import Note


class NoteDeleteView(LoginRequiredMixin, generic.View):
    """Executes secure deletion operations for a workspace note record."""

    def post(self, request, *args, **kwargs):
        """Process target note erasure and handle route redirection."""
        note = get_object_or_404(
            Note,
            pk=self.kwargs["pk"],
            workspace__owner=request.user,
        )
        workspace_id = note.workspace.id
        note.delete()
        return redirect("workspace-detail", pk=workspace_id)