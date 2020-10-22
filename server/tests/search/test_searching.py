from rest_framework.test import APIClient
import pytest

from authentication.models import AppUser
from blog.models import Post
from search.models import Tag


@pytest.fixture
def populate_db():
    user = AppUser.objects.create_user(
        username="test_user",
        password="complex_password12345",
    )

    new_user = AppUser.objects.create_user(
        username="new_user",
        password="another_complex_password123",
        email="new_user@testing.com"
    )

    t1 = Tag.objects.create(name="Testing")
    t2 = Tag.objects.create(name="Sample tag")
    t3 = Tag.objects.create(name="Another tag")

    p1 = Post.objects.create(
        title="Post 1",
        content="This is the first post",
        author=user,
    )

    p1.tags.add(t1, t3)

    p2 = Post.objects.create(
        title="Post 2",
        content="This is the second post",
        author=user,
    )

    p2.tags.add(t1, t2)

    p3 = Post.objects.create(
        title="Post 3",
        content="This is the third post",
        author=new_user,
    )

    p3.tags.add(t2)


@pytest.mark.django_db
class TestSearching:
    client = APIClient()

    def test_get_all_tags(self, populate_db):
        request = self.client.get("/api/v0/tags/")
        assert request.data["count"] == 3

    def test_get_all_posts_with_tag(self, populate_db):
        request = self.client.get("/api/v0/search/by-tag/Another tag/")
        assert request.data["count"] == 1

    def test_get_all_posts_from_user(self, populate_db):
        request = self.client.get("/api/v0/search/by-author/test_user/")
        assert request.data["count"] == 2
