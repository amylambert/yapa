from django.db import models
from workspaces.models import Workspace


class Task(models.Model):
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