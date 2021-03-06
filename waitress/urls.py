from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import routers

from app.views import (ChangePasswordHandler, DailyReportHandler, Dashboard,
                       LoginHandler, LogoutHandler, WeeklyReportHandler,
                       schema_view)
from app.viewsets import MealSessionViewSet, ReportViewSet, UserViewSet
from pantry.viewsets import PantryViewSet

router = routers.SimpleRouter()
router.register(r"meal-sessions", MealSessionViewSet)
router.register(r"users", UserViewSet)
router.register(r"reports", ReportViewSet)
router.register(r"pantry", PantryViewSet)

app_namespace = "waitress"

urlpatterns = [
    path("", LoginHandler.as_view(), name="login"),
    path("dashboard", Dashboard.as_view(), name="dashboard"),
    path("logout", LogoutHandler.as_view(), name="logout"),
    re_path("reports/daily", DailyReportHandler.as_view(), name="daily_report"),
    re_path("reports/weekly", WeeklyReportHandler.as_view(), name="weekly_report"),
    path("change_password", ChangePasswordHandler.as_view(), name="change_password"),
    path("", include((router.urls, app_namespace), namespace="api")),
    path(
        "/", include((router.urls, app_namespace), namespace="api2")
    ),  # hack because the mobile app makes use of //
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
