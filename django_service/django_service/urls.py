from django.contrib import admin
from django.urls import path, include
from app.views import MetricsView, RootView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),
    path("metrics/", MetricsView.as_view(), name="metrics"),
    path("", RootView.as_view(), name="root"),
]
