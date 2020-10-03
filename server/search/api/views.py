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

# TODO: Pagination

class SearchByTagView(APIView):

    permission_classes = [ permissions.AllowAny ]

    def get(self, request, name, format=None):
        # TODO: Select related
        tag = Tag.objects.filter(name=name)
        if tag.exists():
            queryset = tag.first().posts.all()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(data=[])


class SearchByAuthor(APIView):
    permission_classes = [AllowAny]

    def get(self, request, name, format=None):
        try:
            # TODO: Selected related
            user = AppUser.objects.get(username=name)
            queryset = Post.objects.filter(author=user)
            return Response(PostSerializer(queryset, many=True).data)
        except ObjectDoesNotExist:
            raise NotFound()