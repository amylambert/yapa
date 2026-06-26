from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views import generic
from ..models import Project


class ProjectInlineUpdateView(LoginRequiredMixin, generic.View):
    """Controller handling asynchronous background edits for projects."""

    def post(self, request, *args, **kwargs):
        """Process partial project fields sent via AJAX fetch requests."""
        project = get_object_or_404(
            Project,
            pk=self.kwargs["pk"],
            owner=request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        allowed_fields = ["name", "description", "start_date", "end_date"]
        if field in allowed_fields:
            if field in ["start_date", "end_date"]:
                if not value or value.startswith("No"):
                    value = None
                else:
                    value = parse_date(value)

            try:
                setattr(project, field, value)
                project.save()
                return JsonResponse({"status": "success"})
            except ValidationError as error:
                return JsonResponse(
                    {"status": "error", "message": error.message_dict},
                    status=400,
                )

        return JsonResponse(
            {"status": "error", "message": "Invalid field mutation"},
            status=400,
        )