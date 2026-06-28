from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import generic


class AccountUpdateView(LoginRequiredMixin, generic.View):
    """Asynchronously modifies distinct string fields from live pages."""

    def post(self, request, *args, **kwargs):
        """Sanitize and write incoming parameters to user record."""
        if not request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "error"}, status=400)

        field = request.POST.get("field")
        value = request.POST.get("value", "").strip()
        user = request.user

        if field not in ["username", "email"]:
            return JsonResponse({"status": "error"}, status=400)

        if field == "username":
            if not value:
                return JsonResponse({"status": "error"}, status=400)
            user.username = value
        elif field == "email":
            user.email = value

        try:
            user.full_clean()
            user.save()
            return JsonResponse({"status": "success"})
        except ValidationError:
            return JsonResponse({"status": "error"}, status=400)