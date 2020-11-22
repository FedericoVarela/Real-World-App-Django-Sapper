from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from ..models import AppUser


class UserCreateSerializer(ModelSerializer):
    """ 
    Serializer for creating users
    Should not be publicly accessible as it contains sensitive data
    """
    class Meta:
        model = AppUser
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if not "password" in validated_data:
            raise ValidationError({"password": ["This field is required"]})
        user = AppUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(ModelSerializer):
    """ 
    Serializer with the full user public information
    """
    class Meta:
        model = AppUser
        fields = ("username", "created_at", "description", "picture",)
        read_only_fields = ("created_at",)


class MinimalUserSerializer(ModelSerializer):
    """ 
    Serializer for displaying the user as the author of a post or comment
    """
    class Meta:
        model = AppUser
        fields = ("username", "picture")


class ChangePasswordSerializer(Serializer):
    """ Serializer for changing a user's password """
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class UsernameSerializer(Serializer):
    """ Equivalent to DocReferenceSerializer for users, because user's ID isn't public """
    username = CharField()
