from django.test import Client
import pytest

client = Client()

def test_index():
    res = client.get("")
    assert res.status_code == 200

