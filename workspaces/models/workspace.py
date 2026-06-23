from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Workspace(models.Model):
    """Represents an isolated organizational workspace with timelines."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # High-level macro milestones for tracking project lifecycles
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspaces",
    )

    class Meta:
        """Model configuration and metadata options."""

        app_label = "workspaces"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.name)

    def clean(self):
        """Enforce strict chronological validation on macro timelines."""
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    {"end_date": "End date cannot precede the start date."}
                )

    def save(self, *args, **kwargs):
        """Force validation cleaning before committing to the database."""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def root_tasks(self):
        """Retrieve top-level workspace tasks, filtering out sub-tasks."""
        return self.tasks.filter(parent__isnull=True)

    @property
    def root_notes(self):
        """Retrieve only top-level notes to build the base hierarchy."""
        return self.notes.filter(parent__isnull=True)