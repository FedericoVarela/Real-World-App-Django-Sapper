from django.urls import path

from .api import views

urlpatterns = [
    path("following/", views.FollowingView.as_view(), name="following"),
    path("following/<str:username>/", views.UnfollowUserView.as_view(), name="unfollow"),
    path("settings/", views.UpdateSettingsView.as_view(), name="settings"),
    path("profile/<str:username>/", views.UserProfileView.as_view(), name="profile")
]