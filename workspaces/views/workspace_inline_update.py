from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
        value = request.POST.get("value")

        # Explicit whitelist safeguard to prevent unauthorized mutations
        allowed_fields = ["name", "description"]
        if field in allowed_fields:
            setattr(workspace, field, value)
            workspace.save()
            return JsonResponse({"status": "success"})

        return JsonResponse(
            {"status": "error", "message": "Invalid field mutation"},
            status=400,
        )