from authentication.api.serializers import MinimalUserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from common.exceptions import get_key_or_400
from ..models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, CommentCreateSerializer


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
            raise NotFound()
        comments = post.comments.all()
        return Response(CommentSerializer(instance=comments, many=True).data)

    def post(self, request, pk, format=None):
        content = get_key_or_400(request, "content")
        reply_to = request.data.get("reply_to", None)

        # Validate reply
        try:
            valid_ids = Post.objects.get(
                pk=pk).comments.values_list("id", flat=True)
            reply = valid_ids.get(pk=reply_to) if reply_to != None else None
        except ObjectDoesNotExist:
            raise ParseError({"reply_to": ["Invalid comment ID"]})

        data = {"content": content, "reply_to": reply}
        data["post"] = pk
        data["author"] = request.user.pk
        serializer = CommentCreateSerializer(
            data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            user = MinimalUserSerializer(instance=request.user)
            return Response({**serializer.data, "author": user.data})
        return Response(serializer.errors, status=400)


class DeleteCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, format=None):
        pk = get_key_or_400(request, "pk")
        queryset = Comment.objects.filter(pk=pk)
        if queryset.exists():
            instance = queryset.first()
            if instance.author.pk == request.user.pk:
                instance.delete()
            else:
                raise PermissionDenied()
        else:
            raise NotFound()
        return Response(status=204)


class FavoritePostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        my_favorites = request.user.favorites.all()
        return Response(PostSerializer(my_favorites, many=True).data)

    def post(self, request, format=None):
        pk = get_key_or_400(request, "id")
        if not Post.objects.filter(pk=pk).exists():
            raise NotFound()
        request.user.favorites.add(pk)
        return Response({"msg": "OK", }, status=204)

    def delete(self, request, format=None):
        pk = get_key_or_400(request, "id")
        try:
            post = Post.objects.get(pk=pk)
            request.user.favorites.remove(post)
        except ObjectDoesNotExist:
            raise NotFound()
        return Response(status=204)


class Feed(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        following = request.user.following.prefetch_related("posts").all()
        queryset = Post.objects.filter(author__in=following)
        return Response(PostSerializer(queryset, many=True).data)