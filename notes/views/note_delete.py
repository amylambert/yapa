from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse
from ..models import Note


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Explicitly executes deletion of a target documentation node safely."""

    model = Note
    template_name = "notes/note_confirm_delete.html"

    def get_queryset(self):
        """Restrict deletion targets strictly to the resource author."""
        return Note.objects.filter(project__owner=self.request.user)

    def get_success_url(self):
        """Return the user back onto the main parent project dashboard view."""
        return reverse(
            "project-detail",
            kwargs={"pk": self.object.project.id},
        )