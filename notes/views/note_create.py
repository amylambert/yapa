from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from projects.models import Project
from tasks.models import Task
from ..models import Note, Tag


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles structural creation of root notes and sub-notes."""

    model = Note
    fields = ["name", "description", "priority", "start_date", "end_date"]
    template_name = "notes/note_form.html"

    def get_form(self, form_class=None):
        """Pre-populate relational objects before validation occurs."""
        form = super().get_form(form_class)
        form.instance.owner = self.request.user
        project_id = self.kwargs.get("project_id")
        task_parent_id = self.request.GET.get("task_parent")

        # Context A: Note is within an explicit project container
        if project_id:
            project_instance = get_object_or_404(
                Project,
                pk=project_id,
                owner=self.request.user,
            )
            form.instance.project = project_instance

            parent_id = self.request.GET.get("parent")
            if parent_id:
                form.instance.parent = get_object_or_404(
                    Note, pk=parent_id, project=project_instance
                )

            if task_parent_id:
                form.instance.related_task = get_object_or_404(
                    Task, pk=task_parent_id, project=project_instance
                )

        # Context B: Note is standalone (Outside projects)
        else:
            if task_parent_id:
                form.instance.related_task = get_object_or_404(
                    Task, pk=task_parent_id, owner=self.request.user
                )

            parent_id = self.request.GET.get("parent")
            if parent_id:
                form.instance.parent = get_object_or_404(
                    Note, pk=parent_id, owner=self.request.user
                )

        return form

    def form_valid(self, form):
        """Process metadata tags after successful validation."""
        response = super().form_valid(form)
        tag_data = self.request.POST.get("custom_tags", "")

        if tag_data:
            tag_names = [
                t.strip().lower() for t in tag_data.split(",") if t.strip()
            ]
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(
                    name=name, owner=self.request.user
                )
                self.object.tags.add(tag_obj)

        return response

    def get_success_url(self):
        """Redirect back to the correct macro structural context."""
        project_id = self.kwargs.get("project_id")
        task_parent_id = self.request.GET.get("task_parent")
        parent_id = self.request.GET.get("parent")

        # Project redirections
        if project_id:
            if task_parent_id:
                return reverse(
                    "task-detail",
                    kwargs={
                        "project_pk": project_id,
                        "pk": task_parent_id,
                    },
                )
            if parent_id:
                return reverse(
                    "note-detail",
                    kwargs={"project_id": project_id, "pk": parent_id},
                )
            return reverse("project-detail", kwargs={"pk": project_id})

        # Standalone redirections
        if task_parent_id:
            return reverse("task-detail", kwargs={"pk": task_parent_id})
        if parent_id:
            return reverse("note-detail", kwargs={"pk": parent_id})

        return reverse("core:dashboard")