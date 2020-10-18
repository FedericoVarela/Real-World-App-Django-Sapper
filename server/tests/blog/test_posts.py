import pytest
from rest_framework.test import APIClient

from authentication.models import AppUser
from blog.models import Post, Comment
from search.models import Tag


@pytest.fixture
def populate_db():
    user = AppUser.objects.create_user(
        username="test_user",
        password="complex_password12345",
    )
    p1 = Post.objects.create(
        title="Post 1",
        content="This is the first post",
        author=user,
    )
    Post.objects.create(
        title="Post 2",
        content="This is the second post",
        author=user,
    )
    Post.objects.create(
        title="Post 3",
        content="This is the third post",
        author=user,
    )

    c1 = Comment.objects.create(
        content="First comment",
        author=user,
        post=p1,
        reply_to=None
    )
    Comment.objects.create(
        content="Reply to first comment",
        author=user,
        post=p1,
        reply_to=c1
    )
    Tag.objects.create(name="Testing")
    return user


@pytest.mark.django_db
class TestEndPoints:

    client = APIClient()

    def test_get_post_list(self, populate_db):
        request = self.client.get("/api/v0/posts/")
        assert request.data["count"] == 3

    def test_author_is_added_correctly(self):
        user = AppUser.objects.create_user(
            username="new_user",
            password="another_complex_password123",
            email="new_user@testing.com"
        )
        self.client.force_authenticate(user=user)

        request = self.client.post("/api/v0/posts/", {
            "title": "Another post",
            "content": "Sample content",
        })
        assert request.status_code == 201
        assert Post.objects.last().author == user

    def test_tags_are_added(self, populate_db):
        user = populate_db
        self.client.force_authenticate(user=user)
        self.client.post("/api/v0/posts/", {
            "title": "Another post",
            "content": "Sample content",
            "tags[0]": "Testing",
            "tags[1]": "Sample tag"

        })
        # One tag already existed, so check that there are now 2 tags
        assert Tag.objects.all().count() == 2
        # Override the default reverse id ordering
        assert Tag.objects.order_by("id").last().name == "Sample tag"

    def test_author_and_id_are_readonly(self, populate_db):
        user = populate_db
        self.client.force_authenticate(user=user)

        fake_author = AppUser.objects.create_user(
            username="new_user",
            password="another_complex_password123",
            email="new_user@testing.com"
        )

        self.client.post("/api/v0/posts/", {
            "id": "200",
            "title": "Impersonating another user",
            "content": "Trying to select arbitrary authors or IDs shouldn't work",
            "author": fake_author,
        })

        post = Post.objects.order_by("id").last()
        assert post.id != 200
        assert post.author != fake_author
