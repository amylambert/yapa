# accounts/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import RegisterView

# Django uses this to build the namespaced routing map
app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        # Explicitly pass the namespaced target to prevent default lookups
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
]