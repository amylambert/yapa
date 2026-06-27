from django.conf import settings
from django.db import models


class Tag(models.Model):
    """User-created custom labels to classify notes across project streams."""

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="note_tags",
    )

    class Meta:
        """Enforce unique tag naming parameters per developer account."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"], name="unique_user_tag"
            )
        ]

    def __str__(self):
        return str(self.name)