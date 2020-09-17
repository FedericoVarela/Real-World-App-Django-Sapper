from django.urls import path, include

from .api.router import router
from .api import views

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>/related/", views.PostRelatedCommentsView.as_view(), name="posts_related")
]