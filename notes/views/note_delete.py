from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from ..models import Note


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Handles secure deletion of specific documentation notes."""

    model = Note
    template_name = "notes/note_confirm_delete.html"

    def get_queryset(self):
        """Restrict deletion targets strictly to the resource owner."""
        return Note.objects.filter(workspace__owner=self.request.user)

    def get_success_url(self):
        """Fallback dynamically to the parent workspace directory."""
        return reverse_lazy(
            "workspace-detail",
            kwargs={"pk": self.object.workspace.id},
        )