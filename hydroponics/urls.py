from django.contrib import admin
from django.urls import include, path

from .env import env

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("hydroponics_manager.urls")),
]

# if env("DEBUG"):
#     urlpatterns += [
#         path("silk/", include("silk.urls", namespace="silk")),
#         path("__debug__/", include("debug_toolbar.urls")),
#
#     ]
