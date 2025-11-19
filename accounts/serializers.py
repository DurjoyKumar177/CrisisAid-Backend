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
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone",
            "profile_picture",
            "facebook_account",
            "location",
            "occupation",
            "role",  # include role
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        role = validated_data.pop("role", "user")  # default user
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False  # inactive until email verification
        user.role = role
        user.save()

        # Email confirmation
        request = self.context.get("request")
        adapter = get_adapter()
        setup_user_email(request, user, [])
        email_address = user.emailaddress_set.first()
        if email_address:
            adapter.send_confirmation_mail(request, email_address, True)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "phone",
            "profile_picture", "facebook_account", "location", "occupation"
        ]
