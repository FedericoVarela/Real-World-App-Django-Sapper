from django.urls import path, include

from .api.router import router
from .api import views

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>/comments/", views.PostRelatedCommentsView.as_view(), name="posts_related"),
    path("favorites/<int:pk>/", views.RemovePostFromFavorites.as_view(), name="favorites_delete"),
    path("favorites/<str:username>/", views.FavoritePostsView.as_view(), name="favorites"),
    path("favorites/", views.AddFavoriteView.as_view(), name="favorites"),
    path("comment/delete/<int:pk>/", views.DeleteCommentView.as_view(), name="delete_comment"),
    path("feed/", views.Feed.as_view(), name="feed")
]   