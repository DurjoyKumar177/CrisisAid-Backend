from rest_framework import serializers
from .models import CrisisUpdate, Comment

class CommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Comment
        fields = [
            "id",
            "user_id",
            "commenter_name",
            "text",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["update", "text"]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CrisisUpdateSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField()
    creator_email = serializers.ReadOnlyField()
    total_comments = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    crisis_title = serializers.ReadOnlyField(source='crisis_post.title')
    
    class Meta:
        model = CrisisUpdate
        fields = [
            "id",
            "crisis_post",
            "crisis_title",
            "created_by",
            "creator_name",
            "creator_email",
            "title",
            "description",
            "update_image",
            "total_comments",
            "comments",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]


class CrisisUpdateListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing (without comments)"""
    creator_name = serializers.ReadOnlyField()
    total_comments = serializers.ReadOnlyField()
    crisis_title = serializers.ReadOnlyField(source='crisis_post.title')
    
    class Meta:
        model = CrisisUpdate
        fields = [
            "id",
            "crisis_post",
            "crisis_title",
            "creator_name",
            "title",
            "description",
            "update_image",
            "total_comments",
            "created_at"
        ]


class CrisisUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisUpdate
        fields = ["crisis_post", "title", "description", "update_image"]
    
    def validate_crisis_post(self, value):
        """Check if user can create update for this crisis post"""
        request = self.context.get('request')
        user = request.user
        
        # Admin can create updates for any post
        if user.is_staff:
            return value
        
        # Post owner can create updates
        if value.owner == user:
            return value
        
        # Check if user is an approved volunteer
        from volunteers.models import VolunteerApplication
        is_approved_volunteer = VolunteerApplication.objects.filter(
            user=user,
            crisis_post=value,
            status='approved'
        ).exists()
        
        if not is_approved_volunteer:
            raise serializers.ValidationError(
                "You must be the post owner or an approved volunteer to create updates."
            )
        
        return value
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)