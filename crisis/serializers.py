from rest_framework import serializers
from .models import CrisisPost, PostSection

class PostSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSection
        fields = ["id", "section_type", "content"]


class CrisisPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    sections = PostSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = CrisisPost
        fields = ["id", "title", "description", "post_type", "owner", "banner_image", "status", "created_at", "updated_at", "sections"]
