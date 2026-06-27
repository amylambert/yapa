from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..models import Note


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays a specific note record, tags, and nested sub-items."""

    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        """Enforce resource isolation checking across the project owner."""
        return Note.objects.filter(
            project__owner=self.request.user
        ).select_related("project")

    def get_context_data(self, **kwargs):
        """Inject structured sub-tasks and sub-notes arrays into context."""
        context = super().get_context_data(**kwargs)
        context["subnotes"] = self.object.children.all()
        # Grabs linked sub-tasks querying through reverse relation definitions
        context["subtasks"] = self.object.sub_tasks.all()
        return context