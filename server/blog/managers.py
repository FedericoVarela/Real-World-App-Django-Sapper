from django.db import models


class PostQueryset(models.QuerySet):

    def add_favorite_count(self):
        return self.annotate(favorite_count=models.Count("favorites"))

    def is_users_favorite(self, user):
        if not user.is_authenticated:
            return self.annotate(is_favorite=models.Value(False, output_field=models.BooleanField()))
        else:
            return self.annotate(is_favorite=models.Case(
                models.When(
                    pk__in=user.favorites.all(
                    ).values_list("pk", flat=True),

                    then=models.Value(True),
                ),
                default=models.Value(False),
                output_field=models.BooleanField()
            ))


class PostManager(models.Manager):

    def get_queryset(self):
        return PostQueryset(self.model, using=self._db)

    def count_favorites(self):
        return self.get_queryset().add_favorite_count()

    def check_favorites(self, user):
        return self.get_queryset().is_users_favorite(user)
