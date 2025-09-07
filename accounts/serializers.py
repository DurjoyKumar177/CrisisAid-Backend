# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "password", "confirm_password",
            "first_name", "last_name", "phone",
            "profile_picture", "facebook_account", "location", "occupation"
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False  # inactive until email verified
        user.save()

        # Send email confirmation via allauth
        request = self.context.get("request")
        adapter = get_adapter()
        setup_user_email(request, user, [])
        adapter.send_confirmation_mail(request, user.emailaddress_set.get(), True)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "phone",
            "profile_picture", "facebook_account", "location", "occupation"
        ]
