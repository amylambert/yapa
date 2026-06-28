from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views import generic
from ..models import Note


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Explicitly executes deletion of a target note node safely."""

    model = Note
    template_name = "notes/note_confirm_delete.html"

    def get_queryset(self):
        """Restrict deletion targets strictly to the resource author."""
        return Note.objects.filter(
            Q(owner=self.request.user) |
            Q(project__owner=self.request.user)
        ).distinct()

    def get_success_url(self):
        """Return user back onto dashboard or global notes list."""
        if self.object.project:
            return reverse(
                "project-detail",
                kwargs={"pk": self.object.project.id},
            )
        return reverse("note-list")