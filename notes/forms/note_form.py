from django import forms
from ..models import Note


class NoteForm(forms.ModelForm):
    """Form definition for initializing and validating Note records."""

    class Meta:
        """Form configuration mapping target model elements."""

        model = Note
        fields = ["title", "content"]