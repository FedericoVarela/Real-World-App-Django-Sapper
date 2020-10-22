from rest_framework import serializers

# ? Note:
# ? This serializers are for documentation purposes.
# ? They detail responses which don't use serializers in a way that `drf-spectacular` can understand them


class ResultSerializer(serializers.Serializer):
    """ 
    Represents the status of an action without associated data
    """
    msg = serializers.CharField(max_length=2)


class ReferenceSerializer(serializers.Serializer):
    """ 
    Represents any object via its ID
    The type of the object depends on the endpoint in which this serializer is used
    """
    id = serializers.IntegerField()


class ContentSerializer(serializers.Serializer):
    """
    Represents the information required to create a comment from an authenticated request
    """
    content = serializers.CharField(max_length=5000)
