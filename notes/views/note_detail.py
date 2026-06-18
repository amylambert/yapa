from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Note


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    """Securely displays a specific note and its child hierarchy."""

    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        """Enforce strict ownership isolation at the database layer."""
        return Note.objects.filter(
            workspace__owner=self.request.user
        ).select_related("workspace")