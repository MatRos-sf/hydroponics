from django.urls import include, path

from .views import (
    HydroponicSystemCreateView,
    HydroponicSystemDeleteView,
    HydroponicSystemDetailView,
    HydroponicSystemListView,
    HydroponicSystemUpdateView,
)

app_name = "hydroponic_system"
urlpatterns = [
    path("", HydroponicSystemListView.as_view(), name="list"),
    path("create/", HydroponicSystemCreateView.as_view(), name="create"),
    path(
        "hydroponicsystem/<int:pk>/",
        include(
            [
                path("", HydroponicSystemDetailView.as_view(), name="detail"),
                path("update/", HydroponicSystemUpdateView.as_view(), name="update"),
                path("delete/", HydroponicSystemDeleteView.as_view(), name="delete"),
            ]
        ),
    ),
]
