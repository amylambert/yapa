from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic


class SettingsView(LoginRequiredMixin, generic.View):
    """Renders and manages structural cryptographic profile changes."""

    template_name = "accounts/settings.html"

    def get(self, request, *args, **kwargs):
        """Render the primary settings account control canvas."""
        form = PasswordChangeForm(user=request.user)
        return render(
            request, 
            self.template_name, 
            {"password_form": form}
        )

    def post(self, request, *args, **kwargs):
        """Process manual core user password change cycles securely."""
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 
                "Security keys updated successfully."
            )
            return redirect("accounts:settings")
        
        return render(
            request, 
            self.template_name, 
            {"password_form": form}
        )