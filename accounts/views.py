from rest_framework import generics
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
    Allows unauthenticated users to create an account.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]


# ------------------- User Profile -------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update logged-in user's profile.
    Only the owner can access/update their profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        return self.request.user


# ------------------- Social Login -------------------
class GoogleLogin(SocialLoginView):
    """Google OAuth2 login"""
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [IsAuthenticatedOrCreateOnly]


class GitHubLogin(SocialLoginView):
    """GitHub OAuth2 login"""
    adapter_class = GitHubOAuth2Adapter
    permission_classes = [IsAuthenticatedOrCreateOnly]
