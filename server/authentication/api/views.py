from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError

from authentication.models import AppUser
from .serializers import UserSerializer


class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = request.user.following.all()
        return Response(UserSerializer(queryset, many=True).data)

    def post(self, request, format=None):
        username = request.data.get("username")
        if not username:
            raise ParseError(
                {"msg": "Request missing username", "status": 400})

        if not AppUser.objects.filter(username=username).exists():
            raise NotFound({"msg": "Not found", "status": 404})
        pk = AppUser.objects.get(username=username).pk
        request.user.following.add(pk)
        return Response({"msg": "OK", "status": 200})

    def delete(self, request, format=None):
        username = request.data.get("username")
        if not username:
            raise ParseError({"msg": "Request missing username", "status": 400})
        pk = AppUser.objects.get(username=username).pk
        request.user.following.remove(pk)
        return Response({"msg": "OK", "status": 204})
