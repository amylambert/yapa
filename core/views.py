import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from notes.models import Note


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    """Renders the primary authenticated landing framework."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        """Injects environmental variables and notes into context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context["calendar_embed_url"] = os.environ.get(
            "GOOGLE_CALENDAR_EMBED_URL", ""
        )
        
        # Query directly by owner to capture both project and standalone notes
        context["latest_notes"] = Note.objects.filter(
            owner=user
        ).order_by("-id")[:5]
        
        return context