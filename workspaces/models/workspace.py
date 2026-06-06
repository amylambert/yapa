from django.conf import settings
from django.db import models


class Workspace(models.Model):
    """Represents an isolated organizational workspace for tasks."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspaces",
    )

    class Meta:
        """Metadata options for the Workspace model."""

        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return a string representation of the workspace."""
        return str(self.name)