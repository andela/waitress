from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from app.viewsets import MealSessionViewSet, UserViewSet, ReportViewSet
from app.admin import admin_site
from app.views import schema_view, login_handler, dashboard


router = routers.SimpleRouter()
router.register(r"meal-sessions", MealSessionViewSet)
router.register(r"users", UserViewSet)
router.register(r"reports", ReportViewSet)

app_namespace = "waitress"

urlpatterns = [
    path("", login_handler, name="login"),
    path("dashboard", dashboard, name="dashboard"),
    path("", include((router.urls, app_namespace), namespace="api")),
    path(
        "/", include((router.urls, app_namespace), namespace="api2")
    ),  # hack because the mobile app makes use of //
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
