# accounts/urls.py
from django.urls import path
from .views import RegisterView, ProfileView, GoogleLogin, GitHubLogin

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # Social logins
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("github/", GitHubLogin.as_view(), name="github_login"),
]
