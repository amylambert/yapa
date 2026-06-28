from django.core.exceptions import ValidationError
from django.db import models
from core.models.blueprint import ComponentBlueprint
from projects.models import Project
from .tag import Tag


class Note(ComponentBlueprint):
    """Represents an atomic document supporting hierarchical nesting."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes")
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Ensure note scheduling matches macro project parameters."""
        super().clean()
        
        # Check DB column identifier directly to avoid descriptor crashes
        if not self.project_id:
            return

        proj = self.project
        if self.start_date and proj.start_date:
            if self.start_date < proj.start_date:
                raise ValidationError(
                    {"start_date": "Start date precedes project start."}
                )
        if self.end_date and proj.end_date:
            if self.end_date > proj.end_date:
                raise ValidationError(
                    {"end_date": "End date exceeds project boundary."}
                )

    def save(self, *args, **kwargs):
        """Force comprehensive model validations before writing to DB."""
        self.full_clean()
        super().save(*args, **kwargs)