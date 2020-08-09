from django.urls import path, include

from .api.router import router

urlpatterns = [
    path("", include(router.urls)),
]