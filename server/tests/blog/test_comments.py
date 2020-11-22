import pytest
from rest_framework.test import APIClient

from authentication.models import AppUser
from blog.models import Post, Comment

# TODO: silk is making the tests fail

@pytest.fixture
def populate_db():
    user = AppUser.objects.create_user(
        username="test_user", password="complex_password12345")
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
    return user


@pytest.mark.django_db
class TestComments:
    client = APIClient()

    def test_get_related_comments(self, populate_db):
        request = self.client.get("/api/v0/posts/1/comments/")
        assert request.data["count"] == 2

    def test_post_related_comment(self, populate_db):
        user = populate_db
        data = {
            "content": "Another reply to the first comment",
            "reply_to": 1
        }
        self.client.force_authenticate(user=user)
        request = self.client.post(
            "/api/v0/posts/1/comments/", data, format="json")
        response = request.data
        assert response["author"]["username"] == user.username
        assert response["reply_to"] == 1

    def test_invalid_comments_id_fails(self, populate_db):
        user = populate_db
        data = {
            "content": "Invalid reply",
            "reply_to": 4
        }
        self.client.force_authenticate(user=user)
        request = self.client.post(
            "/api/v0/posts/1/comments/", data, format="json")
        assert request.status_code == 400
