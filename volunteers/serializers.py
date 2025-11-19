from rest_framework import serializers
from .models import VolunteerApplication
from crisis.serializers import CrisisPostListSerializer  # Import from crisis app

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.ReadOnlyField()  # Use property
    crisis_title = serializers.ReadOnlyField()  # Use property
    user_id = serializers.ReadOnlyField(source='user.id')
    crisis_post_id = serializers.ReadOnlyField(source='crisis_post.id')
    
    class Meta:
        model = VolunteerApplication
        fields = [
            "id", 
            "user_id",
            "volunteer_name", 
            "crisis_post_id",
            "crisis_title", 
            "message",  # NEW
            "status", 
            "applied_at"
        ]


class VolunteerApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = ["crisis_post", "message"]  # NEW: Include message

    def validate_crisis_post(self, value):
        """Check if post is approved before allowing volunteer application"""
        if value.status != 'approved':
            raise serializers.ValidationError("You can only volunteer for approved crisis posts.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class VolunteerApplicationDetailSerializer(serializers.ModelSerializer):
    """Detailed view with full crisis post info"""
    volunteer_name = serializers.ReadOnlyField()
    crisis_post_detail = CrisisPostListSerializer(source='crisis_post', read_only=True)
    
    class Meta:
        model = VolunteerApplication
        fields = [
            "id", 
            "volunteer_name", 
            "crisis_post_detail", 
            "message", 
            "status", 
            "applied_at"
        ]