from django.db import models
from django.core.exceptions import ValidationError
from core.models.blueprint import ComponentBlueprint
from projects.models import Project


class Task(ComponentBlueprint):
    """Represents an actionable task or nested note within a workspace."""

    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TODO",
    )

    # Time tracking metrics mapped in total minutes
    time_estimate = models.PositiveIntegerField(
        default=0,
        help_text="Estimated time to complete task in minutes.",
    )
    time_spent = models.PositiveIntegerField(
        default=0,
        help_text="Actual time spent working on task in minutes.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadata configurations inheriting baseline sorting frameworks."""
        app_label = "tasks"
        ordering = ["end_date", "priority", "-created_at"]

    def __str__(self) -> str:
        return str(self.name)

    def clean(self):
        """Ensure task deadlines fit within workspace macro schedules."""
        super().clean()

        # Safely resolve workspace context during validation stages
        project_instance = None
        try:
            project_instance = self.project
        except Project.DoesNotExist:
            try:
                project_instance = self.parent.project if self.parent else None
            except AttributeError:
                project_instance = None

        # Validate chronological context mapping boundaries
        if project_instance and self.end_date:
            if project_instance.start_date and self.end_date < project_instance.start_date:
                raise ValidationError(
                    {"end_date": "Task target cannot precede project start."}
                )
            if project_instance.end_date and self.end_date > project_instance.end_date:
                raise ValidationError(
                    {"end_date": "Task target cannot exceed project lifecycle."}
                )

    def save(self, *args, **kwargs):
        """Force complete model validation before database commits."""
        self.full_clean()
        super().save(*args, **kwargs)