from enum import auto
import pytest
from rest_framework.test import APIClient

from authentication.models import AppUser
from blog.models import Post, Tag

client = APIClient()

@pytest.mark.django_db
class TestEndPoints:

    @pytest.fixture(scope="session", autouse=True)
    def populate_db(self):
        user = AppUser.objects.create_user(username="test_user", password="complex_password12345")
        tag = Tag.objects.create(name="Sports")
        Post.objects.create(
            title="Post 1",
            content="This is the first post",
            author=user,
            tag=None,
        )
        Post.objects.create(
            title="Post 2",
            content="This is the second post",
            author=user,
            tag=tag,
            draft=True
        )
        Post.objects.create(
            title="Post 3",
            content="This is the third post",
            author=user,
            tag=tag
        )


    def test_get_post_list():
        request = client.get("/api/v0/blog/posts/")
        print(request.data)
        assert len(request.data) == 2
