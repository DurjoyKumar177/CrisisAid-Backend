from rest_framework import viewsets, permissions, filters
from .models import CrisisPost
from .serializers import CrisisPostSerializer
from .permissions import IsOwnerOrReadOnly

class CrisisPostViewSet(viewsets.ModelViewSet):
    queryset = CrisisPost.objects.all().order_by('-created_at')
    serializer_class = CrisisPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "post_type"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
