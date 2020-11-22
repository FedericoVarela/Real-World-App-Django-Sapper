from rest_framework import serializers

from authentication.models import AppUser

# ? Note:
# ? This serializers are for documentation purposes and they're prefixed with "Doc" to facilitate spotting them in the code
# ? They detail responses which don't use serializers in a way that `drf-spectacular` can understand them


class DocResultSerializer(serializers.Serializer):
    """ 
    Represents the status of an action without associated data
    """
    msg = serializers.CharField(max_length=2)


class DocReferenceSerializer(serializers.Serializer):
    """ 
    Represents any object via its ID
    The type of the object depends on the endpoint in which this serializer is used
    """
    id = serializers.IntegerField()


class DocContentSerializer(serializers.Serializer):
    """
    Represents the information required to create a comment from an authenticated request
    """
    content = serializers.CharField(max_length=5000)


class DocUserProfileSerializer(serializers.ModelSerializer):
    """ 
    Serializer with the full user public information plus `is_following`, 
    which tracks if the current logged in user is following the user in the profile
    """
    is_following = serializers.BooleanField()

    class Meta:
        model = AppUser
        fields = ("username", "created_at", "description",
                  "picture", "is_following")
        read_only_fields = ("created_at",)
