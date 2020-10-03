from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()

router.register("posts", PostViewset, basename="post")
