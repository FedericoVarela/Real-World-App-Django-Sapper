from django.core.exceptions import ObjectDoesNotExist 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import NotFound

from .serializers import CommentSerializer
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
            raise NotFound()
        comments = post.comments.all()
        return Response(CommentSerializer(instance=comments, many=True).data)


    def post(self, request, pk, format=None):
        request_data = request.data.__getitem__("content")
        data = {"content": request_data}
        data["post"] = pk
        data["author"] = request.user.pk
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
