from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from ..models import Task


class TaskInlineUpdateView(LoginRequiredMixin, generic.View):
    """Controller handling background AJAX updates for task fields."""

    def post(self, request, *args, **kwargs):
        """Process partial field updates sent via asynchronous fetch."""
        task = get_object_or_404(
            Task,
            pk=self.kwargs["pk"],
            workspace__owner=self.request.user,
        )

        field = request.POST.get("field")
        value = request.POST.get("value")

        # Explicit safeguard constraint updated for choices
        allowed_fields = ["title", "description", "status", "priority"]
        if field in allowed_fields:
            setattr(task, field, value)
            task.save()
            return JsonResponse({"status": "success"})

        return JsonResponse(
            {"status": "error", "message": "Invalid field mutation"},
            status=400,
        )