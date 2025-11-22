from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwner, IsAuthenticatedOrCreateOnly

# Social login imports
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

User = get_user_model()


# ------------------- Custom Registration -------------------
class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ------------------- User Profile -------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update logged-in user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user


# ------------------- Social Login -------------------
class GoogleLogin(SocialLoginView):
    """Google OAuth2 login"""
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [AllowAny]  # Changed - Allow anyone


class GitHubLogin(SocialLoginView):
    """GitHub OAuth2 login"""
    adapter_class = GitHubOAuth2Adapter
    permission_classes = [AllowAny]  # Changed - Allow anyone