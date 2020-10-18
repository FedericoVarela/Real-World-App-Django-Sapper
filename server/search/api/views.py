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


class SearchByTagView(APIView):
    """
    Get all posts associated to a tag
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, name, format=None):
        tag = Tag.objects.filter(name=name).prefetch_related("posts")
        if tag.exists():
            queryset = tag.first().posts.all()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(data=[])


class SearchByAuthor(APIView):
    """ 
    Get all posts created by a user
    """
    permission_classes = [AllowAny]

    def get(self, request, name, format=None):
        try:
            user_qs = AppUser.objects.filter(
                username=name).prefetch_related("posts")
            user = user_qs.first()
            queryset = Post.objects.filter(author=user)
            return Response(PostSerializer(queryset, many=True).data)
        except ObjectDoesNotExist:
            raise NotFound()
