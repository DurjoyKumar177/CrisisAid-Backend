from rest_framework import generics, permissions
from .models import VolunteerApplication
from .serializers import VolunteerApplicationSerializer, VolunteerApplicationCreateSerializer
from .permissions import IsPostOwnerOrReadOnly, IsVolunteerOwner
from rest_framework.response import Response

# Apply for volunteering
class ApplyVolunteerView(generics.CreateAPIView):
    serializer_class = VolunteerApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

# List all volunteer applications for logged-in user
class UserVolunteerApplicationsView(generics.ListAPIView):
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VolunteerApplication.objects.filter(user=self.request.user)


# Approve or Reject Volunteer (Only post owner)
class ApproveRejectVolunteerView(generics.UpdateAPIView):
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerOrReadOnly]
    queryset = VolunteerApplication.objects.all()

    def patch(self, request, *args, **kwargs):
        action = request.data.get("action")
        if action not in ["approve", "reject"]:
            return Response({"error": "Invalid action"}, status=400)

        instance = self.get_object()
        instance.status = "approved" if action == "approve" else "rejected"
        instance.save()
        return Response({"success": f"Volunteer {instance.user.username} {instance.status}"})
