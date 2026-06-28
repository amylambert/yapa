from django.contrib.auth import views as auth_views
from django.urls import path
from .views.register import RegisterView
from .views.settings import SettingsView
from .views.account_update import AccountUpdateView

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
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "settings/",
        SettingsView.as_view(),
        name="settings",
    ),
    path(
        "settings/update/",
        AccountUpdateView.as_view(),
        name="update-account",
    ),
]