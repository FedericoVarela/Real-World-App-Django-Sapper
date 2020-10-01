from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from authentication.models import AppUser
from .serializers import UserSerializer
from common.exceptions import get_key_or_400

class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = request.user.following.all()
        return Response(UserSerializer(queryset, many=True).data)

    def post(self, request, format=None):
        username = get_key_or_400(request, "username")

        if not AppUser.objects.filter(username=username).exists():
            raise NotFound()
        pk = AppUser.objects.get(username=username).pk
        request.user.following.add(pk)
        return Response({"username": username, "id": pk})


    def delete(self, request, format=None):
        username = get_key_or_400(request, "username")
        pk = AppUser.objects.get(username=username).pk
        request.user.following.remove(pk)
        return Response({"username": username, "id": pk})

# TODO: update user