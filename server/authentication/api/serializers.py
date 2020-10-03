from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from ..models import AppUser

class UserCreateSerializer(HyperlinkedModelSerializer):
    """ 
    Serializer for creating users
    Should not be publicly accessible as it contains sensitive data
    """
    class Meta:
        model = AppUser
        fields = ("username", "created_at", "email", "password")


class UserProfileSerializer(HyperlinkedModelSerializer):
    """ 
    Serializer with the full user public information
    """
    class Meta:
        model = AppUser
        fields = ("username", "created_at", "description", "picture",)


class SafeUserSerializer(HyperlinkedModelSerializer):
    """ 
    Serializer for updating the user's safe fields
    """
    class Meta:
        model = AppUser
        fields = ("description", "picture")

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.save()
        return instance


class MinimalUserSerializer(ModelSerializer):

    class Meta:
        model = AppUser
        fields = ("username", "picture")