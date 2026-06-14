import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from ..models import Note


class NoteInlineUpdateView(LoginRequiredMixin, generic.View):
    """Asynchronously modifies note attributes via partial AJAX streams."""

    def post(self, request, *args, **kwargs):
        """Validate ownership rules and execute partial attribute updates."""
        note = get_object_or_404(
            Note,
            pk=self.kwargs["pk"],
            workspace__owner=request.user,
        )

        try:
            data = json.loads(request.body)
            field = data.get("field")
            value = data.get("value")
        except (json.JSONDecodeError, TypeError):
            return JsonResponse(
                {"error": "Malformed configuration payload."}, status=400
            )

        # White-list fields allowed to be modified asynchronously
        if field not in ["title", "content"]:
            return JsonResponse(
                {"error": "Target attribute modification restricted."},
                status=400,
            )

        try:
            setattr(note, field, value)
            note.full_clean()
            note.save()
        except ValidationError as error:
            return JsonResponse({"error": error.message_dict}, status=400)

        return JsonResponse({"status": "success", "value": value})