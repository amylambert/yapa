from django.db import models
from django.core.exceptions import ValidationError
from core.models.schedulable import SchedulableModel
from workspaces.models import Workspace


class Task(SchedulableModel):
    """Represents an actionable task or nested note within a workspace."""

    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    # Self-referential key allowing tasks to contain nested sub-tasks
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subtasks",
    )
    # Cross-relational reference enabling notes to contain sub-tasks
    related_note = models.ForeignKey(
        "notes.Note",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_tasks",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TODO",
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
    )
    due_date = models.DateField(blank=True, null=True)

    # Time tracking metrics mapped in total minutes
    time_estimate = models.PositiveIntegerField(
        default=0,
        help_text="Estimated time to complete task in minutes.",
    )
    time_spent = models.PositiveIntegerField(
        default=0,
        help_text="Actual time spent working on task in minutes.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadata configuration options for the Task entity."""

        ordering = ["due_date", "priority"]

    def __str__(self) -> str:
        return str(self.title)

    def clean(self):
        """Ensure task deadlines fit within workspace macro schedules."""
        super().clean()

        # Safely resolve workspace context during form validation stages
        workspace = None
        try:
            workspace = self.workspace
        except Task.workspace.RelatedObjectDoesNotExist:
            # Fallback to the parent task's workspace if creating a subtask
            try:
                workspace = self.parent.workspace if self.parent else None
            except Task.parent.RelatedObjectDoesNotExist:
                workspace = None

        # Only run boundary validations if the workspace context is available
        if workspace and getattr(self, "deadline", None):
            task_date = self.deadline.date()
            if workspace.start_date and task_date < workspace.start_date:
                raise ValidationError(
                    {"deadline": "Task cannot precede workspace start."}
                )
            if workspace.end_date and task_date > workspace.end_date:
                raise ValidationError(
                    {"deadline": "Task cannot exceed workspace end."}
                )

    def save(self, *args, **kwargs):
        """Force complete model validation before database commits."""
        self.full_clean()
        super().save(*args, **kwargs)