from django.db import models
from workspaces.models import Workspace


class Note(models.Model):
    """Represents a dedicated documentation or text file inside a workspace."""

    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database indexing configurations and collection sorting options."""

        app_label = "notes"
        ordering = ["-updated_at"]

    def __str__(self):
        """Return a clean string normalization of the note identifier."""
        return str(self.title)