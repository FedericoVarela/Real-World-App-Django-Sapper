from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Tag
from .serializers import TagSerializer


class TagViewset(ReadOnlyModelViewSet):
    """ 
    list: List of all tags
    read: Get a tag by ID
    """
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer