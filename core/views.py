import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    """Renders the primary authenticated landing framework."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        """Injects required environmental variables into template scope."""
        context = super().get_context_data(**kwargs)
        
        # Read the environment string cleanly using the OS system wrapper
        context["calendar_embed_url"] = os.environ.get(
            "GOOGLE_CALENDAR_EMBED_URL", ""
        )
        
        return context