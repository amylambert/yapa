import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views import generic
from notes.models import Note
from tasks.models import Task


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    """Renders the primary authenticated landing framework."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        """Injects core dashboard metrics and target deadline profiles."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        
        context["calendar_embed_url"] = os.environ.get(
            "GOOGLE_CALENDAR_EMBED_URL", ""
        )
        
        # Pull latest notes owned directly or via nested projects
        context["latest_notes"] = Note.objects.filter(
            Q(owner=user) | Q(project__owner=user)
        ).order_by("-id")[:5]
        
        # Pull 5 closest incomplete tasks with valid future deadlines
        context["urgent_tasks"] = Task.objects.filter(
            Q(owner=user) | Q(project__owner=user),
            end_date__gte=today
        ).exclude(
            status="DONE"
        ).order_by("end_date")[:5]
        
        return context