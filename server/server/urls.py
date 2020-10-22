from decouple import config
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

import blog.urls as blog_urls
import authentication.urls as auth_urls
import search.urls as search_urls


DEBUG = config("DEBUG")
ADMIN_URL = config("ADMIN_URL")

urlpatterns = [
    path("", TemplateView.as_view(template_name="server/index.html"), name="home"),
    path(f"{ADMIN_URL}/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/v0/", include([
        path("jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("", include(auth_urls)),
        path("", include(blog_urls)),
        path("", include(search_urls)),
    ])),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
