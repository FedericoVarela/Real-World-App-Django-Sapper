from decouple import config
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

import blog.urls as blog_urls
import authentication.urls as auth_urls

DEBUG = config("DEBUG")

urlpatterns = [
    path("", TemplateView.as_view(template_name="server/index.html"), name="home"),
    path("admin/", admin.site.urls),
    path("api/v0/", include([
        path("", include('djoser.urls')),
        path("", include('djoser.urls.jwt')),
        path("blog/", include(blog_urls)),
        path("", include(auth_urls))
    ])),

]

if DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
