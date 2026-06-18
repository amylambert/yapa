from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.dateparse import parse_datetime
from ..models import Note


class NoteInlineUpdateView(LoginRequiredMixin, View):
    """Handles secure, asynchronous generic updates for note attributes."""

    def post(self, request, *args, **kwargs):
        """Process generic field/value payloads from the client safely."""
        note = get_object_or_404(
            Note,
            pk=self.kwargs.get("pk"),
            workspace__owner=request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        # Strict security whitelist to block unauthorized model injection
        if field not in ["title", "content", "deadline"]:
            return JsonResponse({"status": "error"}, status=400)

        # Handle unique attribute types cleanly
        if field == "deadline":
            if not value or value.startswith("No"):
                note.deadline = None
            else:
                note.deadline = parse_datetime(value)
        else:
            setattr(note, field, value)

        note.save()
        return JsonResponse({"status": "success"})