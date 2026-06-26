from core.models import ComponentBlueprint


class Project(ComponentBlueprint):
    """Represents an isolated operational project with encrypted data fields."""

    class Meta:
        app_label = "projects"
        # Explicitly maps native database fields
        ordering = ["priority", "end_date", "-created_at"]

    def save(self, *args, **kwargs):
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