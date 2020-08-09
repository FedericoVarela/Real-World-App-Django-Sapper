from rest_framework.serializers import HyperlinkedModelSerializer

from ..models import Comment, Post, Tag
from authentication.api.serializers import UserSerializer


class TagSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class PostSerializer(HyperlinkedModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        # Don't include draft field as every visible post is bound to have draft=False
        fields = ("title", "content", "author", "tag")
        depth = 1


class PostCreateSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "tag", "draft")

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        return Post(**validated_data, author=author)


class CommentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", "post", "reply_to")

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        return Comment(**validated_data, author=author)

