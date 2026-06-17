from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration lifecycle management for the shared core subsystem."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"