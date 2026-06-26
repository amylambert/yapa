import base64
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet


class EncryptedTextField(models.TextField):
    """
    Custom model field that automatically handles symmetrical encryption
    UNUSED FOR NOW.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Derive a valid 32-byte URL-safe base64 key from Django's SECRET_KEY safely
        key = settings.SECRET_KEY.encode().ljust(32)[:32]
        self.cipher = Fernet(base64.urlsafe_b64encode(key))

    def get_prep_value(self, value):
        """Encrypt plain text parameters right before they touch the database."""
        value = super().get_prep_value(value)
        if value is not None and value != "":
            return self.cipher.encrypt(value.encode()).decode()
        return value

    def from_db_value(self, value, expression, connection):
        """Decrypt encrypted database blocks instantly back into string values."""
        if value is not None and value != "":
            try:
                return self.cipher.decrypt(value.encode()).decode()
            except Exception:
                return value  # Fallback gracefully if string isn't encrypted
        return value