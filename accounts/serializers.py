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

class UserProfileSerializer(serializers.ModelSerializer):
    # Add a field to check if user logged in via social auth
    is_social_user = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'phone', 
            'profile_picture', 
            'facebook_account', 
            'location', 
            'occupation',
            'role',
            'date_joined',
            'is_social_user'
        ]
        read_only_fields = ['id', 'date_joined', 'role']
    
    def get_is_social_user(self, obj):
        """Check if user has social account"""
        return obj.socialaccount_set.exists()
    
    def validate_username(self, value):
        """Prevent username change for social auth users"""
        if self.instance and self.instance.socialaccount_set.exists():
            if value != self.instance.username:
                raise serializers.ValidationError(
                    "Cannot change username for social login accounts."
                )
        return value
    
    def validate_email(self, value):
        """Prevent email change for social auth users"""
        if self.instance and self.instance.socialaccount_set.exists():
            if value != self.instance.email:
                raise serializers.ValidationError(
                    "Cannot change email for social login accounts."
                )
        return value
    
    def update(self, instance, validated_data):
        """Update user profile with proper handling of profile picture"""
        # Handle profile picture upload
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            # Delete old profile picture if exists
            if instance.profile_picture:
                try:
                    instance.profile_picture.delete(save=False)
                except:
                    pass
            instance.profile_picture = profile_picture
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance