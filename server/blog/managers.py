from django.db import models


class PostQueryset(models.QuerySet):
    
    def add_favorite_count(self):
        return self.annotate(favorite_count=models.Count("favorites"))


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQueryset(self.model, using=self._db)

    def count_favorites(self):
        return self.get_queryset().add_favorite_count()