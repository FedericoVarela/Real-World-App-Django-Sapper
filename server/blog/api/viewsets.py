from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import *


def public_read_private_write(action):
    if action == "list" or action == "retrieve":
        permission_classes = [AllowAny]
    else:
        permission_classes = [IsAuthenticated]
    return [permission() for permission in permission_classes]


class PostViewset(ModelViewSet):
    queryset = Post.objects.filter(draft=False)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


    def list(self, request):
        serializer = PostSerializer(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)


    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ensure the user attempting to update is the author
        if request.user.pk == instance.author.pk:
            instance.title = request.data.__getitem__("title")
            instance.content = request.data.__getitem__("content")
            instance.save()
            serializer = PostSerializer(instance=instance)
            return Response(serializer.data)

        raise PermissionDenied({"msg": "Forbidden"})

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().destroy(self, request, *args, **kwargs)
        raise PermissionDenied({"msg": "Forbidden"})

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            # If we are creating a Post, use the serializer that auto adds the user
            return PostCreateSerializer
        else:
            return PostSerializer

    def get_permissions(self):
        return public_read_private_write(self.action)


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()

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

    def get_permissions(self):
        return public_read_private_write(self.action)


class TagViewset(ModelViewSet):
    queryset = Tag.objects.all()

