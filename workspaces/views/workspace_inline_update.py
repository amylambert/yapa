from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views import generic
from ..models import Workspace


class WorkspaceInlineUpdateView(LoginRequiredMixin, generic.View):
    """Controller handling asynchronous background edits for workspaces."""

    def post(self, request, *args, **kwargs):
        """Process partial workspace fields sent via AJAX fetch requests."""
        workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs["pk"],
            owner=request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()

        # Explicit whitelist safeguard to prevent unauthorized mutations
        allowed_fields = ["name", "description", "start_date", "end_date"]
        if field in allowed_fields:
            # Sanitize and parse incoming date parameters safely
            if field in ["start_date", "end_date"]:
                if not value or value.startswith("No"):
                    value = None
                else:
                    value = parse_date(value)

            try:
                setattr(workspace, field, value)
                workspace.save()
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