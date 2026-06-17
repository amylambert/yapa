import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404
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

        try:
            data = json.loads(request.body)
            field = data.get("field")
            value = data.get("value")
        except (json.JSONDecodeError, TypeError):
            return JsonResponse(
                {"error": "Malformed configuration payload."}, status=400
            )

        # Allow deadline modifications alongside core task blocks
        if field not in ["title", "status", "deadline"]:
            return JsonResponse(
                {"error": "Target attribute modification restricted."},
                status=400,
            )

        # Sanitize empty datetime values for database compatibility
        if field == "deadline" and value == "":
            value = None

        try:
            setattr(task, field, value)
            task.full_clean()
            task.save()
        except ValidationError as error:
            return JsonResponse({"error": error.message_dict}, status=400)

        # Format return value for clean frontend UI substitution
        if field == "status":
            display_val = task.get_status_display()
        else:
            display_val = value if value else "No deadline set."

        return JsonResponse({"status": "success", "value": display_val})