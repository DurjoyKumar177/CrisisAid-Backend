# accounts/views.py
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

# Social login imports
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

User = get_user_model()


# ------------------- Custom Registration -------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ------------------- Social Login -------------------
class GoogleLogin(SocialLoginView):
    """Google OAuth2 login"""
    adapter_class = GoogleOAuth2Adapter


class GitHubLogin(SocialLoginView):
    """GitHub OAuth2 login"""
    adapter_class = GitHubOAuth2Adapter
