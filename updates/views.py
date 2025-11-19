from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CrisisUpdate, Comment
from crisis.models import CrisisPost
from .serializers import (
    CrisisUpdateSerializer,
    CrisisUpdateListSerializer,
    CrisisUpdateCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer
)
from .permissions import IsUpdateCreatorOrReadOnly, IsCommentOwnerOrReadOnly, CanCreateUpdate


# Create Crisis Update
class CreateCrisisUpdateView(generics.CreateAPIView):
    serializer_class = CrisisUpdateCreateSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateUpdate]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "success": "Crisis update created successfully!",
            "data": CrisisUpdateSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)


# List All Updates for a Crisis (Timeline)
class CrisisUpdatesListView(generics.ListAPIView):
    serializer_class = CrisisUpdateListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        crisis_id = self.kwargs.get('crisis_id')
        return CrisisUpdate.objects.filter(crisis_post_id=crisis_id)


# Get Single Update with Comments
class CrisisUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrisisUpdate.objects.all()
    serializer_class = CrisisUpdateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUpdateCreatorOrReadOnly]


# My Updates (Created by logged-in user)
class MyUpdatesView(generics.ListAPIView):
    serializer_class = CrisisUpdateListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CrisisUpdate.objects.filter(created_by=self.request.user)


# Create Comment on Update
class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "success": "Comment added successfully!",
            "data": CommentSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)


# List Comments for an Update
class UpdateCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        update_id = self.kwargs.get('update_id')
        return Comment.objects.filter(update_id=update_id)


# Update/Delete Comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "success": "Comment updated successfully!",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": "Comment deleted successfully!"
        }, status=status.HTTP_204_NO_CONTENT)


# My Comments
class MyCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)