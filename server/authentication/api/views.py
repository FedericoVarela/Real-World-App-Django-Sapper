from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from drf_spectacular.utils import extend_schema

from authentication.models import AppUser
from .serializers import ChangePasswordSerializer, UserCreateSerializer, UserProfileSerializer, UsernameSerializer
from common.exceptions import get_key_or_400
from common.serializers import ResultSerializer
from common.views import PaginatedAPIView
from common.decorators import pagination_parameters


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


class FollowingView(PaginatedAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @pagination_parameters
    def get(self, request, format=None):
        """ List of all users followed by the current user """
        queryset = request.user.following.all()
        paginated = self.paginate_queryset(queryset)
        return self.get_paginated_response(UserProfileSerializer(paginated, many=True).data)

    @extend_schema(request=UsernameSerializer)
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
    @extend_schema(responses={204: ResultSerializer})
    def delete(self, request, username, format=None):
        """ Unfollow another user """
        pk = AppUser.objects.get(username=username).pk
        request.user.following.remove(pk)
        return Response({"msg": "OK"}, status=204)


class UpdateSettingsView(APIView):
    """ Update the current user's profile """
    serializer_class = UserProfileSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        raise ParseError(serializer.errors)


class RegisterUserView(APIView):
    """ Register a new user """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        raise ParseError(serializer.errors)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer

    @extend_schema(responses={200: ResultSerializer})
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user 
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Incorrect password."]}, status=400)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"msg": "OK"}, status=200)

        raise ParseError(serializer.errors)
