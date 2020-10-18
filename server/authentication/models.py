from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    email       = models.EmailField(max_length=50, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    favorites   = models.ManyToManyField("blog.Post", related_name="favorites")
    following   = models.ManyToManyField("self", related_name="following")
    description = models.CharField(max_length=500, blank=True, default="", help_text="Short user bio")
    picture     = models.URLField(default="https://static.productionready.io/images/smiley-cyrus.jpg", max_length=2000, help_text="Profile picture URL")
