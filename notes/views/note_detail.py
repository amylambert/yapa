from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Note


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    """Renders a dedicated detail panel for a specific note document."""

    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        """Ensure notes are isolated to the authenticated workspace owner."""
        return Note.objects.filter(workspace__owner=self.request.user)