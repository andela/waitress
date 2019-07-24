from app.viewsets import MealSessionViewSet, UserViewSet, ReportViewSet
from app.admin import admin_site
from app.views import SwaggerSchemaView

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'meal-sessions', MealSessionViewSet)
router.register(r'users', UserViewSet)
router.register(r'reports', ReportViewSet)

app_namespace = 'waitress'

urlpatterns = [
    path('', include((router.urls, app_namespace), namespace='api',)),
    path('docs/', SwaggerSchemaView.as_view()),
    path('admin/', admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
