from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, IntegerField, ListSerializer, BooleanField

from ..models import Comment, Post
from authentication.api.serializers import MinimalUserSerializer
from search.models import Tag
from search.api.serializers import TagSerializer


class StringListSerializer(ListSerializer):
    child = CharField(max_length=100)

# TODO: is_favorite still doesn't work
class PostSerializer(ModelSerializer):
    author = MinimalUserSerializer(help_text="Post title")
    tags = TagSerializer(many=True, help_text="Associated tags")
    favorite_count = IntegerField()
    is_favorite = BooleanField()

    class Meta:
        model = Post
        fields = "__all__"
        depth = 1

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.content = validated_data.get("content", instance.content)

    #     tags = validated_data.get("tags", None)
    #     if not tags is None:
    #         tag_list = []
    #         for name in tags:
    #             tag = Tag.objects.get_or_create(name=name)
    #             tag_list.append(tag[0].id)
    #         instance.tags.set(tag_list)

    #     instance.save()
    #     return instance


class PostCreateSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    tags = StringListSerializer(required=False, help_text="List of tag names")

    class Meta:
        model = Post
        fields = ("id", "title", "content", "tags",
                  "created_at", "modified_at",)
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

        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)

        tags = validated_data.get("tags", None)
        if not tags is None:
            tag_list = []
            for name in tags:
                tag = Tag.objects.get_or_create(name=name)
                tag_list.append(tag[0].id)
            instance.tags.set(tag_list)

        instance.save()
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
