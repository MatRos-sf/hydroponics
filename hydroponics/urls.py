from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("hydroponics_manager.urls")),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
