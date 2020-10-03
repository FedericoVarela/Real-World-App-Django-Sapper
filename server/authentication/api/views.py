from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError

from authentication.models import AppUser
from .serializers import UserCreateSerializer, SafeUserSerializer
from common.exceptions import get_key_or_400

class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = request.user.following.all()
        return Response(UserCreateSerializer(queryset, many=True).data)

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


class UpdateSettingsView(APIView):
    
    def patch(self, request, format=None):
        serializer = SafeUserSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        raise ParseError(serializer.errors)


# TODO: JWT logout
# TODO: user readonly viewset, with favorites