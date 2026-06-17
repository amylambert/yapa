from django.db import models


class SchedulableModel(models.Model):
    """Abstract structural layer equipping models with calendar sync features."""

    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timezone-aware deadline target timestamp.",
    )
    calendar_event_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        help_text="Remote calendar unique tracking resource token reference.",
    )

    class Meta:
        """Enforce purely abstract inheritance behaviors."""

        abstract = True