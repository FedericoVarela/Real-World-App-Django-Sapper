from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .serializers import PostSerializer, PostCreateSerializer
from ..models import Post
from common.pagination import PostListPagination
from common.serializers import DocResultSerializer


class PostViewset(ModelViewSet):

    queryset = Post.objects.prefetch_related(
        "tags").select_related("author").add_favorite_count().order_by("-id") # Default ordering doesn't work on Viewsets
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    pagination_class = PostListPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """ List of all posts """
        page = self.paginate_queryset(
            self.queryset.is_users_favorite(request.user))
        if page is not None:
            serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, context={"request": request})
        return Response(serializer.data)

    @extend_schema(request=PostCreateSerializer)
    def partial_update(self, request, *args, **kwargs):
        """ Update any number of fields on a post """
        instance = self.get_object()
        # Ensure the user attempting to update is the author
        if request.user.pk == instance.author.pk:
            serializer = PostCreateSerializer(instance=instance)
            serializer.update(instance, request.data)
            return Response(serializer.data)
        raise PermissionDenied()

    @extend_schema(responses={204: DocResultSerializer})
    def destroy(self, request, *args, **kwargs):
        """ Deletes a post """
        instance = self.get_object()
        if request.user == instance.author:
            self.perform_destroy(instance)
            return Response({"msg": "OK"}, status=204)
        raise PermissionDenied()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            # If we are creating a Post, use the serializer that auto adds the user
            return PostCreateSerializer
        else:
            return PostSerializer
