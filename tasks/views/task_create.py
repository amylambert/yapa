from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from projects.models import Project
from notes.models import Note
from ..models import Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Handles secure generation of tasks nested under projects, tasks, or notes."""

    model = Task
    fields = [
        "name", 
        "status", 
        "start_date", 
        "end_date", 
        "priority", 
        "description", 
        "time_estimate"
    ]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        """Bind task to its structural parent layers and current owner context."""
        project_id = self.kwargs.get("project_pk")
        project_instance = get_object_or_404(
            Project,
            pk=project_id,
            owner=self.request.user,
        )
        
        form.instance.project = project_instance
        form.instance.owner = self.request.user

        # Scenario A: Initialized as a subtask under another task node
        parent_id = self.request.GET.get("parent")
        if parent_id:
            parent_task = get_object_or_404(
                Task, pk=parent_id, project=project_instance
            )
            form.instance.parent = parent_task

        # Scenario B: Initialized under documentation notes
        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            related_note = get_object_or_404(
                Note, pk=note_parent_id, project=project_instance
            )
            form.instance.related_note = related_note

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user back to the correct context page."""
        project_id = self.kwargs.get("project_pk")
        
        note_parent_id = self.request.GET.get("note_parent")
        if note_parent_id:
            return reverse("note-detail", kwargs={"pk": note_parent_id})

        parent_id = self.request.GET.get("parent")
        if parent_id:
            return reverse(
                "task-detail",
                kwargs={
                    "project_pk": project_id,
                    "pk": parent_id,
                },
            )

        return reverse(
            "project-detail",
            kwargs={"pk": project_id},
        )