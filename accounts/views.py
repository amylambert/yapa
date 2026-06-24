# accounts/views.py
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
        # Save user to database
        redirect_response = super().form_valid(form)
        # Log session in automatically
        login(self.request, self.object)
        return redirect_response