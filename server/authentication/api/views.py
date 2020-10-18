from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError

from authentication.models import AppUser
from .serializers import SafeUserSerializer, UserProfileSerializer
from common.exceptions import get_key_or_400


class UserProfileView(APIView):
    """
    Profile of a user given its username
    """
    permission_classes = [AllowAny]

    def get(self, request, name, format=None):
        try:
            user = AppUser.objects.get(username=name)
        except ObjectDoesNotExist:
            raise NotFound()
        return Response(UserProfileSerializer(instance=user).data)


class FollowingView(APIView):
    """ 
    get:    List of all users followed by the current user
    post:   Follow another user
    delete: Unfollow another user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = request.user.following.all()
        return Response(UserProfileSerializer(queryset, many=True).data)

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
        # return Response({"username": username, "id": pk})
        return Response(status=204)


class UpdateSettingsView(APIView):
    """ 
    Update the current user's profile
    """
    def patch(self, request, format=None):
        serializer = SafeUserSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        raise ParseError(serializer.errors)
