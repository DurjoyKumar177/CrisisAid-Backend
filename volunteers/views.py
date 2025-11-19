from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import VolunteerApplication
from crisis.models import CrisisPost
from .serializers import (
    VolunteerApplicationSerializer, 
    VolunteerApplicationCreateSerializer,
    VolunteerApplicationDetailSerializer
)
from .permissions import IsPostOwnerOrReadOnly, IsVolunteerOwner

# Apply for volunteering
class ApplyVolunteerView(generics.CreateAPIView):
    serializer_class = VolunteerApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check for duplicate application
        crisis_post = serializer.validated_data['crisis_post']
        if VolunteerApplication.objects.filter(user=request.user, crisis_post=crisis_post).exists():
            return Response(
                {"error": "You have already applied for this crisis post."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"success": "Application submitted successfully!", "data": serializer.data}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )


# List all volunteer applications for logged-in user
class UserVolunteerApplicationsView(generics.ListAPIView):
    serializer_class = VolunteerApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VolunteerApplication.objects.filter(user=self.request.user)


# List volunteers for a specific crisis post (Post Owner or Admin only)
class CrisisVolunteersListView(generics.ListAPIView):
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        crisis_id = self.kwargs.get('crisis_id')
        crisis_post = get_object_or_404(CrisisPost, id=crisis_id)
        
        # Only post owner or admin can see volunteers
        if self.request.user != crisis_post.owner and not self.request.user.is_staff:
            return VolunteerApplication.objects.none()
        
        return VolunteerApplication.objects.filter(crisis_post=crisis_post)


# Approve Volunteer (Post owner or Admin)
class ApproveVolunteerView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerOrReadOnly]

    def post(self, request, pk):
        application = get_object_or_404(VolunteerApplication, pk=pk)
        self.check_object_permissions(request, application)
        
        if application.status == 'approved':
            return Response(
                {"error": "This application is already approved."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'approved'
        application.save()
        
        return Response({
            "success": f"Volunteer {application.user.username} approved for {application.crisis_post.title}",
            "data": VolunteerApplicationSerializer(application).data
        })


# Reject Volunteer (Post owner or Admin)
class RejectVolunteerView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerOrReadOnly]

    def post(self, request, pk):
        application = get_object_or_404(VolunteerApplication, pk=pk)
        self.check_object_permissions(request, application)
        
        if application.status == 'rejected':
            return Response(
                {"error": "This application is already rejected."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'rejected'
        application.save()
        
        return Response({
            "success": f"Volunteer {application.user.username} rejected for {application.crisis_post.title}",
            "data": VolunteerApplicationSerializer(application).data
        })