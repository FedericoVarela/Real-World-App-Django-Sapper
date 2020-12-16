from django.db import models

from .managers import PostManager


class ModelWithDates(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(ModelWithDates):
    title = models.CharField(max_length=256, help_text="Title of the post")
    content = models.CharField(max_length=10000, help_text="Body of the post")
    author = models.ForeignKey(
        "authentication.AppUser", on_delete=models.SET_NULL, related_name="posts", null=True, help_text="Creator of the post")
    tags = models.ManyToManyField(
        "search.Tag", related_name="posts", blank=True
    )
    
    objects = PostManager()

    class Meta:
        default_related_name = "posts"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"


    def is_users_favorite(self, user) -> bool:
        if not user.is_authenticated:
            return False
        res = user.favorites.filter(id=self.id).exists() 
        self.is_favorite = res
        return res


class Comment(ModelWithDates):
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(
        "authentication.AppUser", on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)

    class Meta:
        default_related_name = "comments"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.author.username}:{self.content[:15]}... at {self.post.title}"
