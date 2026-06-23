from django.core.exceptions import ValidationError
from django.db import models
from core.models.schedulable import SchedulableModel
from workspaces.models import Workspace


class Note(SchedulableModel):
    """Represents an atomic document supporting hierarchical nesting."""

    workspace = models.ForeignKey(
        Workspace,
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
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        """Ensure note deadlines fall within macro workspace ranges."""
        super().clean()
        if self.workspace and self.deadline:
            ws = self.workspace
            note_date = self.deadline.date()
            
            if ws.start_date and note_date < ws.start_date:
                raise ValidationError(
                    {"deadline": "Deadline cannot precede workspace start."}
                )
            if ws.end_date and note_date > ws.end_date:
                raise ValidationError(
                    {"deadline": "Deadline cannot exceed workspace end."}
                )

    def save(self, *args, **kwargs):
        """Force comprehensive model validations before writing to DB."""
        self.full_clean()
        super().save(*args, **kwargs)