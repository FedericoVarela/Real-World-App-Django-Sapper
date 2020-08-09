from blog.models import Post, Comment, Tag
from authentication.models import AppUser
import pytest


@pytest.fixture
def user_and_tag_fixture():
    user = AppUser.objects.create_user(username="test_user", password="complex_password12345")
    tag = Tag.objects.create(name="Sports")
    return user, tag


@pytest.fixture
def user_and_post_fixture():
    user = AppUser.objects.create_user(username="test_user", password="complex_password12345")
    tag = Tag.objects.create(name="Sports")
    data = {
        "title": "Test Post",
        "content": "Lorem ipsum",
        "author": user,
        "tag": tag
    }
    post = Post.objects.create(**data)
    return user, post


@pytest.mark.django_db
class TestModels:

    @staticmethod
    def test_create_tag():
        tag = Tag.objects.create(name="Sports")
        assert Tag.objects.first() == tag


    def test_create_post(self, user_and_tag_fixture):
        author, tag = user_and_tag_fixture
        data = {
            "title": "Test Post",
            "content": "Lorem ipsum",
            "author": author,
            "tag": tag
        }
        post = Post.objects.create(**data)
        from_db = Post.objects.filter(author=author)
        assert from_db.first() == post


    def test_add_comment(self, user_and_post_fixture):
        author, post = user_and_post_fixture
        data = {
            "content": "Lorem ipsum",
            "author": author,
            "post": post,
            "reply_to": None
        }
        comment = Comment.objects.create(**data)
        assert post.comments.first() == comment
