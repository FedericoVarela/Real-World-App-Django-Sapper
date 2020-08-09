from django.db import models


class ModelWithDates(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Post(ModelWithDates):
    title   = models.CharField(max_length=256)
    content = models.CharField(max_length=10000)
    author  = models.ForeignKey("authentication.AppUser", on_delete=models.SET_NULL, related_name="posts", null=True)
    tag     = models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name="posts", null=True, blank=True)
    draft   = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"


class Comment(ModelWithDates):
    content  = models.CharField(max_length=5000)
    author   = models.ForeignKey("authentication.AppUser", on_delete=models.SET_NULL, null=True)
    post     = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
