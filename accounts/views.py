from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .permissions import IsOwner, IsAuthenticatedOrCreateOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

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
class UserProfileView(APIView):
    """
    Get and update user profile.
    Supports file uploads for profile picture.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Support file uploads
    
    def get(self, request):
        """Get user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile"""
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        """Partial update user profile"""
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Social Login -------------------
class GoogleLogin(SocialLoginView):
    """Google OAuth2 login"""
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [AllowAny]  # Changed - Allow anyone


class GitHubLogin(SocialLoginView):
    """GitHub OAuth2 login"""
    adapter_class = GitHubOAuth2Adapter
    permission_classes = [AllowAny]  # Changed - Allow anyone