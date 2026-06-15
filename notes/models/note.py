from django.db import models
from workspaces.models import Workspace


class Note(models.Model):
    """Represents an atomic document supporting hierarchical nesting."""

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="notes"
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