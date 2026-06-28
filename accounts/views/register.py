from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class RegisterView(generic.CreateView):
    """Handles secure user isolation, setup, and immediate login."""

    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        """Process valid submission and log user session in."""
        redirect_response = super().form_valid(form)
        login(self.request, self.object)
        return redirect_response