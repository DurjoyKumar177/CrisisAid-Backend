from rest_framework import serializers
from .models import CrisisPost, PostSection

class PostSectionSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField()  # NEW: Show who created section
    
    class Meta:
        model = PostSection
        fields = ["id", "section_type", "content", "creator_name", "created_at"]


class CrisisPostSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField()  # NEW: Use property
    owner_email = serializers.ReadOnlyField()  # NEW: Use property
    sections = PostSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = CrisisPost
        fields = [
            "id", 
            "title", 
            "description", 
            "post_type", 
            "location",  # NEW
            "owner", 
            "owner_name",  # NEW
            "owner_email",  # NEW
            "banner_image", 
            "status", 
            "created_at", 
            "updated_at", 
            "sections"
        ]
        read_only_fields = ["owner", "status", "created_at", "updated_at"]  # NEW: Prevent users from changing status


class CrisisPostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing posts (without sections)"""
    owner_name = serializers.ReadOnlyField()
    
    class Meta:
        model = CrisisPost
        fields = ["id", "title", "post_type", "location", "owner_name", "status", "created_at", "banner_image"]