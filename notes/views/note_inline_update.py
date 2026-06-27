from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views import View
from ..models import Note


class NoteInlineUpdateView(LoginRequiredMixin, View):
    """Asynchronously updates distinct note field keys via AJAX requests."""

    def post(self, request, *args, **kwargs):
        """Process field/value update payloads securely from clients."""
        note = get_object_or_404(
            Note,
            pk=self.kwargs.get("pk"),
            project__owner=request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        if field not in [
            "name",
            "description",
            "priority",
            "start_date",
            "end_date",
        ]:
            return JsonResponse(
                {"status": "error", "message": "Modification restricted."},
                status=400,
            )

        if field in ["start_date", "end_date"]:
            if not value or value.startswith("No") or value == "None":
                value = None
            else:
                value = parse_date(value)
        else:
            setattr(note, field, value)

        try:
            note.full_clean()
            note.save()
            return JsonResponse({"status": "success"})
        except ValidationError as error:
            return JsonResponse(
                {"status": "error", "message": error.message_dict},
                status=400,
            )