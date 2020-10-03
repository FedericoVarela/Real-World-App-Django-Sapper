from django.urls import path, include

from .api.router import router
from .api import views

urlpatterns = [
    path("", include(router.urls)),
    path("search/", include([
        path("by_tag/<str:name>", views.SearchByTagView.as_view(), name="search_by_tag"),
        path("by_author/<str:name>", views.SearchByAuthor.as_view(), name="search_by_author"),
    ])),
]