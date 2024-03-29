from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from backend.search import views as search_views
from .apis import api_router
from backend.watch import urls as watch_urls
from backend.yechat import urls as yechat_urls
from backend.blog import urls as blog_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

urlpatterns = urlpatterns + [
    path("api/v1/auth/", include("rest_registration.api.urls")),
    path("api/v1/watch/", include(watch_urls)),
    path("api/v1/yechat/", include(yechat_urls)),
    path("api/v1/blog/", include(blog_urls)),
    path("api/v2/", api_router.urls),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
