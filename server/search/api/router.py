from rest_framework.routers import DefaultRouter

from .viewsets import TagViewset

router = DefaultRouter()
router.register("tags", TagViewset, basename="tag")
