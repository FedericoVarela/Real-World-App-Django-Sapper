from rest_framework.serializers import HyperlinkedModelSerializer

from ..models import AppUser

class UserSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = AppUser
        fields = ("username", "created_at")