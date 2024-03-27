from django.contrib.auth.views import LoginView
from django.urls import include, path

from .views import (
    CustomLogoutView,
    HydroponicSystemCreateView,
    HydroponicSystemDeleteView,
    HydroponicSystemDetailView,
    HydroponicSystemListView,
    HydroponicSystemUpdateView,
    SignUpView,
)

app_name = "hydroponic_system"

urlpatterns = [
    path("", HydroponicSystemListView.as_view(), name="list"),
    path(
        "login/",
        LoginView.as_view(template_name="hydroponics_manager/login.html"),
        name="login",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
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
