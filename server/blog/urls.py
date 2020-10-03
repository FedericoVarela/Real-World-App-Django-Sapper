from django.urls import path, include

from .api.router import router
from .api import views

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>/related/", views.PostRelatedCommentsView.as_view(), name="posts_related"),
    path("favorites/", views.FavoritePostsView.as_view(), name="favorites"),
    path("comment/delete", views.DeleteCommentView.as_view(), name="delete_comment"),
    path("feed/", views.Feed.as_view(), name="feed")
]   