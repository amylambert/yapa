from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    """Represents an isolated organizational project with timelines."""

    class Meta:
        """Model configuration and metadata options."""

        app_label = "projects"
        ordering = ["priority", "end_date", "-created_at"]

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

    #@property
    #def root_tasks(self):
    #    """Retrieve top-level project tasks, filtering out sub-tasks."""
    #    return self.tasks.filter(parent__isnull=True)

    #@property
    #def root_notes(self):
    #    """Retrieve only top-level notes to build the base hierarchy."""
    #    return self.notes.filter(parent__isnull=True)