from re import M
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer

from ..models import Comment, Post
from authentication.api.serializers import MinimalUserSerializer
from search.models import Tag
from search.api.serializers import TagSerializer


class StringListSerializer(ListSerializer):
    child = CharField(max_length=100)


class PostSerializer(ModelSerializer):
    author = MinimalUserSerializer(help_text="Post title")
    tags = TagSerializer(many=True, help_text="Associated tags")
    favorite_count = IntegerField()

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1


class PostCreateSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    tags = StringListSerializer(required=False, help_text="List of tag names")

    class Meta:
        model = Post
        fields = ("id", "title", "content", "tags",
                  "created_at", "modified_at")
        read_only_fields = ("id",)

    def create(self, validated_data):
        # Request is passed by the viewset
        author = self.context["request"].user
        tags = validated_data.pop("tags", None)
        instance = Post(**validated_data, author=author)
        instance.save()

        if tags and len(tags):
            tag_ids = []
            for name in tags:
                entry = Tag.objects.get_or_create(name=name)
                tag_ids.append(entry[0].id)
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
        fields = "__all__"
        read_only_fields = ("id", "created_at", "modified_at")
