from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Tag
from .serializers import TagSerializer


class TagViewset(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer