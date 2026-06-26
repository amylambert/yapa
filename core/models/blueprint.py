from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from .fields import EncryptedTextField


class ComponentBlueprint(models.Model):
    """
    Abstract architecture sharing core properties with encrypted properties.
    Ensures zero database-level JOIN overhead during execution loops.
    """

    class PriorityChoices(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    name = EncryptedTextField(max_length=255)
    description = EncryptedTextField(blank=True, null=True)
    
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    {"end_date": "End date cannot precede the start date."}
                )