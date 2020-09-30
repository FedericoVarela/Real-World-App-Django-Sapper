from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .serializers import *
from .pagination import PostListPagination
from common.exceptions import get_key_or_400

class PostViewset(ModelViewSet):
    queryset = Post.objects.filter(draft=False)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    pagination_class = PostListPagination
    permission_classes = [ IsAuthenticatedOrReadOnly ]

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        #TODO: Add all tags and create non existing ones
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ensure the user attempting to update is the author
        if request.user.pk == instance.author.pk:
            instance.title = get_key_or_400(request, "title")
            instance.content = get_key_or_400(request, "content")
            instance.save()
            serializer = PostSerializer(instance=instance)
            return Response(serializer.data)

        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().destroy(self, request, *args, **kwargs)
        raise PermissionDenied()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            # If we are creating a Post, use the serializer that auto adds the user
            return PostCreateSerializer
        else:
            return PostSerializer


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [ IsAuthenticatedOrReadOnly ]

    def list(self, request):
        serializer = CommentSerializer(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        else:
            return CommentSerializer


class TagViewset(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
