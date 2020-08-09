# from django.test import Client
from authentication.models import AppUser
import pytest

@pytest.mark.django_db
def test_create_user():
    user =  AppUser.objects.create_user(username="test_user", password="complex_password12345")
    assert user.username == "test_user"