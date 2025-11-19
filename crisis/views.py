from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CrisisPost
from .serializers import CrisisPostSerializer, CrisisPostListSerializer
from .permissions import IsOwnerOrReadOnly

class CrisisPostViewSet(viewsets.ModelViewSet):
    queryset = CrisisPost.objects.all()
    serializer_class = CrisisPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "post_type", "location"]
    ordering_fields = ["created_at", "updated_at"]
    
    def get_queryset(self):
        """Filter posts: Only approved posts visible to non-staff"""
        queryset = CrisisPost.objects.all()
        
        # Non-staff users see only approved posts
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='approved')
        
        # Filter by post_type if provided
        post_type = self.request.query_params.get('post_type', None)
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        
        # Filter by status if provided (admin only)
        if self.request.user.is_staff:
            status_filter = self.request.query_params.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return CrisisPostListSerializer
        return CrisisPostSerializer
    
    def perform_create(self, serializer):
        """Save post with current user as owner"""
        serializer.save(owner=self.request.user)
    
    # ADMIN-ONLY ACTIONS
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """Admin approves a crisis post"""
        post = self.get_object()
        post.status = 'approved'
        post.save()
        return Response({'status': 'Post approved'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """Admin rejects a crisis post"""
        post = self.get_object()
        post.status = 'rejected'
        post.save()
        return Response({'status': 'Post rejected'}, status=status.HTTP_200_OK)
    
    # USER ACTIONS
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """Get current user's posts"""
        posts = CrisisPost.objects.filter(owner=request.user).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)