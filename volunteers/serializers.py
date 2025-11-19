from rest_framework import serializers
from .models import VolunteerApplication

class VolunteerApplicationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show username
    crisis_post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VolunteerApplication
        fields = ["id", "user", "crisis_post", "status", "applied_at"]


class VolunteerApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = ["crisis_post"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
