from decouple import config
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

import blog.urls as blog_urls
import authentication.urls as auth_urls
import search.urls as search_urls


DEBUG = config("DEBUG")
ADMIN_URL = config("ADMIN_URL")

urlpatterns = [
    path("", TemplateView.as_view(template_name="server/index.html"), name="home"),
    path(f"{ADMIN_URL}/", admin.site.urls),
    path('docs/', include_docs_urls(title='Real World API', permission_classes=[AllowAny])),
    path("api/v0/", include([
        path("", include('djoser.urls')),
        path("", include('djoser.urls.jwt')),
        path("", include(auth_urls)),
        path("", include(blog_urls)),
        path("", include(search_urls)),
    ])),

]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
