from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from drf_spectacular.utils import extend_schema

from authentication.models import AppUser
from .serializers import SafeUserSerializer, UserProfileSerializer
from common.exceptions import get_key_or_400
from common.serializers import ResultSerializer


class UserProfileView(APIView):
    """ Profile of a user given its username """
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer

    def get(self, request, username, format=None):
        try:
            user = AppUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise NotFound()
        return Response(UserProfileSerializer(instance=user).data)


class FollowingView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, format=None):
        """ List of all users followed by the current user """
        queryset = request.user.following.all()
        return Response(UserProfileSerializer(queryset, many=True).data)

    def post(self, request, format=None):
        """ Follow another user """
        username = get_key_or_400(request, "username")

        if not AppUser.objects.filter(username=username).exists():
            raise NotFound()
        user = AppUser.objects.get(username=username)
        pk = user.pk
        request.user.following.add(pk)
        return Response(UserProfileSerializer(instance=user))


class UnfollowUserView(APIView):
    @extend_schema(
        responses={ 204: ResultSerializer }
    )
    def delete(self, request, username, format=None):
        """ Unfollow another user """
        pk = AppUser.objects.get(username=username).pk
        request.user.following.remove(pk)
        return Response({"msg": "OK"}, status=204)


class UpdateSettingsView(APIView):
    """ Update the current user's profile """
    serializer_class = SafeUserSerializer

    def patch(self, request, format=None):
        serializer = SafeUserSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        raise ParseError(serializer.errors)
