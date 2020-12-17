from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.response import Response

from blog.models import Post
from blog.api.serializers import PostSerializer
from authentication.models import AppUser
from ..models import Tag
from common.views import PaginatedAPIView
from common.decorators import pagination_parameters


class SearchByTagView(PaginatedAPIView):
    """ Get all posts associated to a tag """
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer

    @pagination_parameters
    def get(self, request, tag, format=None):   
        tag_obj = Tag.objects.filter(name=tag)
        if tag_obj.exists():
            queryset = tag_obj.prefetch_related("posts").first().posts.select_related(
                "author").prefetch_related("tags").add_favorite_count().is_users_favorite(request.user)
            paginated = self.paginate_queryset(queryset)
            serializer = PostSerializer(
                paginated, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        return Response(data=[])


class SearchByAuthor(PaginatedAPIView): 
    """ Get all posts created by a user """
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    @pagination_parameters
    def get(self, request, username, format=None):
        try:
            user = AppUser.objects.filter(
                username=username).prefetch_related("posts").first()
            queryset = Post.objects.filter(author=user).select_related(
                "author").prefetch_related("tags").add_favorite_count().is_users_favorite(request.user)
            paginated = self.paginate_queryset(queryset)
            return self.get_paginated_response(PostSerializer(paginated, many=True, context={"request": request}).data)
        except ObjectDoesNotExist:
            raise NotFound()
