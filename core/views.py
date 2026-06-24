from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    """Renders the primary authenticated landing framework."""

    template_name = "dashboard.html"