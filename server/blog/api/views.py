from authentication.models import AppUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.exceptions import get_key_or_400
from common.serializers import DocReferenceSerializer, DocResultSerializer, DocContentSerializer
from common.views import PaginatedAPIView
from common.decorators import pagination_parameters
from ..models import Comment, Post
from .serializers import CommentSerializer, PostSerializer, CommentCreateSerializer
from authentication.api.serializers import MinimalUserSerializer


class PostRelatedCommentsView(PaginatedAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentSerializer
    # Only used for identifying the pk in the URL as corresponding to a Post
    queryset = Post.objects.none()

    def get_permissions(self):
        if self.request.method == "GET":
            permission_set = [permissions.AllowAny]
            return [permission() for permission in permission_set]
        else:
            permission_set = [permissions.IsAuthenticated]
            return [permission() for permission in permission_set]

    @pagination_parameters
    def get(self, request, pk, format=None):
        """ Get a paginated response with all comments associated to a post """
        try:
            post = Post.objects.prefetch_related("comments").get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFound()
        comments = post.comments.select_related("author").all()
        paginated = self.paginate_queryset(comments)
        serializer = CommentSerializer(paginated, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(request=DocContentSerializer,)
    def post(self, request, pk, format=None):
        """ Create a comment associated to a post """
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
            date = timezone.now()
            extra_data = {
                "author": user.data,
                "created_at": date,
                "modified_at": date,
            }
            return Response({**serializer.data, **extra_data}, status=201)
        return Response(serializer.errors, status=400)


class DeleteCommentView(APIView):
    """ Deletes a particular comment given its ID """
    permission_classes = [permissions.IsAuthenticated]
    # Fallback
    queryset = Comment.objects.none()

    @extend_schema(responses={204: DocResultSerializer})
    def delete(self, request, pk: int, format=None):
        qs = Comment.objects.filter(pk=pk).select_related("author")
        instance = qs.first()
        if instance is None:
            raise NotFound()

        if instance.author.pk == request.user.pk:
            instance.delete()
        else:
            raise PermissionDenied()
        return Response({"msg": "OK", }, status=204)


class FavoritePostsView(PaginatedAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer

    @pagination_parameters
    def get(self, request, username, format=None):
        """ Get the favorite posts of any given user """
        try:
            user = AppUser.objects.get(username=username)
            queryset = Post.objects.count_favorites().filter(
                favorites__in=[user.id]).select_related("author").prefetch_related("tags").is_users_favorite(request.user)
            paginated = self.paginate_queryset(queryset)
            return self.get_paginated_response(PostSerializer(paginated, many=True, context={"request": request}).data)
        except ObjectDoesNotExist:
            raise NotFound()


class AddFavoriteView(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=DocReferenceSerializer,
        responses={201: DocResultSerializer}
    )
    def post(self, request, format=None):
        """ Add a post to the current user's favorites """
        pk = get_key_or_400(request, "id")
        if not Post.objects.filter(pk=pk).exists():
            raise NotFound()
        request.user.favorites.add(pk)
        return Response({"msg": "OK", }, status=201)


class RemovePostFromFavorites(APIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.none()

    @extend_schema(
        request=DocReferenceSerializer,
        responses={204: DocResultSerializer}
    )
    def delete(self, request, pk, format=None):
        """ Remove a post from favorites """
        try:
            post = Post.objects.get(pk=pk)
            request.user.favorites.remove(post)
        except ObjectDoesNotExist:
            raise NotFound()
        return Response({"msg": "OK", }, status=204)


class Feed(PaginatedAPIView):
    """ Get all posts created by users followed by the current user """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    @pagination_parameters
    def get(self, request, format=None):
        following = request.user.following.prefetch_related("posts").all()
        queryset = Post.objects.filter(author__in=following).prefetch_related(
            "tags").select_related("author").add_favorite_count().is_users_favorite(request.user)
        paginated = self.paginate_queryset(queryset)
        return self.get_paginated_response(PostSerializer(paginated, many=True, context={"request": request}).data)
