from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    email       = models.EmailField(max_length=50)
    description = models.CharField(max_length=500)
    created_at  = models.DateTimeField(auto_now_add=True)
    favorites   = models.ManyToManyField("blog.Post", related_name="favorites")
    following   = models.ManyToManyField("self", related_name="following")