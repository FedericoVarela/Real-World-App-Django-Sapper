from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ParseError

from .serializers import CommentSerializer, PostSerializer
from ..models import Post


class PostRelatedCommentsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_set = [permissions.AllowAny]
            return [permission() for permission in permission_set]
        else:
            permission_set = [permissions.IsAuthenticated]
            return [permission() for permission in permission_set]

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.prefetch_related("comments").get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound({"msg": "Not found", "status": 404})
        comments = post.comments.all()
        return Response(CommentSerializer(instance=comments, many=True).data)

    def post(self, request, pk, format=None):
        content = request.data.__getitem__("content")
        reply_to = request.data.__getitem__("reply_to")

        # Validate reply
        try:
            valid_ids = Post.objects.get(
                pk=pk).comments.values_list("id", flat=True)
            reply = valid_ids.get(pk=reply_to)
        except ObjectDoesNotExist:
            raise ParseError({"msg": "Invalid comment ID", "status": 400})

        data = {"content": content, "reply_to": reply}
        data["post"] = pk
        data["author"] = request.user.pk
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class FavoritePostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None) -> Response:
        my_favorites = request.user.favorites.all()
        return Response(PostSerializer(my_favorites, many=True).data)

    def post(self, request, format=None) -> Response:
        pk = request.data.__getitem__("id")
        if not Post.objects.filter(pk=pk).exists():
            raise NotFound({"msg": "Not found", "status": 404})
        request.user.favorites.add(pk)
        return Response({"msg": "OK", "status": 204})

    def delete(self, request, format=None):
        pk = request.data.__getitem__("id")
        try:
            post = Post.objects.get(pk=pk)
            request.user.favorites.remove(post)
        except ObjectDoesNotExist:
            raise NotFound({"msg": "Not found", "status": 404})
        return Response({"msg": "OK", "status": 204})
