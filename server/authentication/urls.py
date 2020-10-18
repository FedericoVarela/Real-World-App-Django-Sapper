from django.urls import path

from .api import views

urlpatterns = [
    path("following/", views.FollowingView.as_view(), name="following"),
    path("settings/", views.UpdateSettingsView.as_view(), name="settings"),
    path("profile/<str:name>", views.UserProfileView.as_view(), name="profile")
]