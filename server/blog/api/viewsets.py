from typing import ContextManager
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *


class PostViewset(ModelViewSet):
    queryset = Post.objects.filter(draft=False)

    def list(self, request):
        serializer = PostSerializer(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            # If we are creating a Post, use the serializer that auto adds the user
            return PostCreateSerializer
        else:
            return PostSerializer
    
    def get_permissions(self):
        if self.action == "list" or self.action == "get":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes ]


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()

    def list(self, request):
        serializer = CommentSerializer(self.queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        else:
            return CommentSerializer


class TagViewset(ModelViewSet):
    queryset = Tag.objects.all()

    # def list(self, request):

