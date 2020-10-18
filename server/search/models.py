from django.db import models
from django.db.models.expressions import OrderBy


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name
