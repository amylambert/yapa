from django.conf import settings
from django.db import models


class Workspace(models.Model):
    """Represents an isolated organizational workspace."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
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
    
    @property
    def root_tasks(self):
        """Retrieve only top-level workspace tasks, filtering out sub-tasks."""
        return self.tasks.filter(parent__isnull=True)