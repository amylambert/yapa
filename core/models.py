from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class ComponentBlueprint(models.Model):
    """
    Abstract base architectural model sharing core systemic attributes.
    Ensures zero database-level JOIN overhead during model instantiation.
    """

    class PriorityChoices(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )

    # Chronological lifecycle tracking anchors
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # related_name is dynamically evaluated using subclass app identifiers
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        """Declares this class as a code-only abstraction layout structural model."""
        abstract = True

    def __str__(self):
        return str(self.name)

    def clean(self):
        """Enforce standard chronological validation across all child modules."""
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    {"end_date": "End date cannot precede the start date."}
                )