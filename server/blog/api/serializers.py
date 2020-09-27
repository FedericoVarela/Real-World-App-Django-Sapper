from rest_framework.serializers import ModelSerializer, IntegerField
# from rest_framework.exceptions import PermissionDenied

from ..models import Comment, Post, Tag
from authentication.api.serializers import UserSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class PostSerializer(ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        # Don't include draft field as every visible post is bound to have draft=False
        fields = ("id", "title", "content", "author", "tag")
        depth = 1


class PostCreateSerializer(ModelSerializer):
    id = IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "tag", "draft")

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        instance = Post(**validated_data, author=author)
        instance.save()
        return instance

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("reply_to", "content", "post")

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        instance = Comment(**validated_data, author=author)
        instance.save() 
        return instance

