from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from ..models import Task


class TaskInlineUpdateView(LoginRequiredMixin, generic.View):
    """Asynchronously modifies task attributes via partial AJAX streams."""

    def post(self, request, *args, **kwargs):
        """Validate ownership rules and execute partial attribute updates."""
        task = get_object_or_404(
            Task,
            pk=self.kwargs["pk"],
            workspace__owner=request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        # Expand whitelist to fully match all editable template fields securely
        if field not in [
            "title",
            "status",
            "description",
            "priority",
            "deadline",
        ]:
            return JsonResponse(
                {"error": "Target attribute modification restricted."},
                status=400,
            )

        # Sanitize empty datetime values for database compatibility
        if field == "deadline":
            if not value or value.startswith("No"):
                value = None
            else:
                value = parse_datetime(value)

        try:
            setattr(task, field, value)
            task.full_clean()
            task.save()
        except ValidationError as error:
            return JsonResponse({"error": error.message_dict}, status=400)

        return JsonResponse({"status": "success"})