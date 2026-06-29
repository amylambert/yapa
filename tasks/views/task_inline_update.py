from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views import generic
from ..models import Task


class TaskInlineUpdateView(LoginRequiredMixin, generic.View):
    """Asynchronously modifies task attributes via partial AJAX streams."""

    def post(self, request, *args, **kwargs):
        """Validate ownership rules and execute partial attribute updates."""
        # Securely match standalone assets or project-scoped assets
        task = get_object_or_404(
            Task,
            Q(owner=request.user) | Q(project__owner=request.user),
            pk=self.kwargs["pk"],
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        if field not in [
            "name",
            "status",
            "description",
            "priority",
            "start_date",
            "end_date",
        ]:
            return JsonResponse(
                {"error": "Target attribute modification restricted."},
                status=400,
            )

        if field in ["start_date", "end_date"]:
            if not value or value.startswith("No") or value == "None":
                value = None
            else:
                value = parse_date(value)

        try:
            setattr(task, field, value)
            task.full_clean()
            task.save()
        except ValidationError as error:
            return JsonResponse({"error": error.message_dict}, status=400)

        return JsonResponse({"status": "success"})