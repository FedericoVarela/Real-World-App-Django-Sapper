from django.urls import path

from .api import views

urlpatterns = [
    path("following/", views.FollowingView.as_view(), name="following")
]