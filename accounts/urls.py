# accounts/urls.py
from django.urls import path,include
from .views import RegisterView, GoogleLogin, GitHubLogin
from . import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('auth/', include('dj_rest_auth.urls')),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),

    # Social logins
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("github/", GitHubLogin.as_view(), name="github_login"),
]
