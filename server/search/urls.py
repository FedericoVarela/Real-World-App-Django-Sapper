from django.urls import path, include

from .api import views

urlpatterns = [
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("search/", include([
        path("by_tag/<str:name>/", views.SearchByTagView.as_view(), name="search_by_tag"),
        path("by_author/<str:username>/", views.SearchByAuthor.as_view(), name="search_by_author"),
    ])),
]