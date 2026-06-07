from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .models import Workspace


class RegisterView(generic.CreateView):
    """Handles new user registration using Django's standard form structure."""

    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class WorkspaceListView(LoginRequiredMixin, generic.ListView):
    """Controller displaying workspaces for the logged-in user."""

    model = Workspace
    template_name = "workspaces/workspace_list.html"
    context_object_name = "workspaces"

    def get_queryset(self):
        """Filter workspaces to ensure users only see their own records."""
        return Workspace.objects.filter(owner=self.request.user)
    
class WorkspaceCreateView(LoginRequiredMixin, generic.CreateView):
    """Controller for creating a new workspace under the current user."""

    model = Workspace
    fields = ["name", "description"]
    template_name = "workspaces/workspace_form.html"
    success_url = reverse_lazy("workspace-list")

    def form_valid(self, form):
        """Automatically assign the logged-in user as the owner."""
        form.instance.owner = self.request.user
        return super().form_valid(form)