from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
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
    def get(self, request, name, format=None):
        tag = Tag.objects.filter(name=name).prefetch_related("posts")
        if tag.exists():
            queryset = tag.first().posts.all()
            paginated = self.paginate_queryset(queryset)
            serializer = PostSerializer(paginated, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(data=[])


class SearchByAuthor(PaginatedAPIView):
    """ Get all posts created by a user """
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    @pagination_parameters
    def get(self, request, username, format=None):
        #TODO: Optimization; This page uses 44 SQL queries
        try:
            user_qs = AppUser.objects.filter(
                username=username).prefetch_related("posts")
            user = user_qs.first()
            queryset = Post.objects.filter(author=user)
            paginated = self.paginate_queryset(queryset)
            return self.get_paginated_response(PostSerializer(paginated, many=True).data)
        except ObjectDoesNotExist:
            raise NotFound()
