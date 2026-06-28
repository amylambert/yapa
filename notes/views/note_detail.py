from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import generic
from ..models import Note


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    """Displays a specific note record, tags, and nested sub-items."""

    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        """Enforce resource isolation checking across the user space."""
        return Note.objects.filter(
            Q(owner=self.request.user) | 
            Q(project__owner=self.request.user)
        ).select_related("project").distinct()

    def get_context_data(self, **kwargs):
        """Inject structured sub-tasks and sub-notes arrays into context."""
        context = super().get_context_data(**kwargs)
        context["subnotes"] = self.object.children.all()
        # Grabs linked sub-tasks querying through reverse relations
        context["subtasks"] = self.object.sub_tasks.all()
        return context