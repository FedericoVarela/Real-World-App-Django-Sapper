from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer

from ..models import Comment, Post
from authentication.api.serializers import MinimalUserSerializer
from search.models import Tag
from search.api.serializers import TagSerializer


class StringListSerializer(ListSerializer):
    child = CharField(max_length=100)


class PostSerializer(ModelSerializer):
    author = MinimalUserSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class PostCreateSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    tags = StringListSerializer()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("id", "author")

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        tags = validated_data.pop("tags", None)
        instance = Post(**validated_data, author=author)
        tag_ids = []
        for name in tags:
            entry = Tag.objects.get_or_create(name=name)
            tag_ids.append(entry[0].id)
        instance.save()
        instance.tags.add(*tag_ids)

        # Gets the user
        # Gets every tag individually
        # Insert post
        # Insert the tags, probably using the intermediate table

        return instance


class CommentSerializer(ModelSerializer):
    author = MinimalUserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "reply_to", "content", "post")
        read_only_fields = ("id",)

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        instance = Comment(**validated_data, author=author)
        instance.save()
        return instance
