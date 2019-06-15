from app.viewsets import MealSessionViewSet, UserViewSet, ReportViewSet
from app.admin import admin_site

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view


router = routers.SimpleRouter()
router.register(r'meal-sessions', MealSessionViewSet)
router.register(r'users', UserViewSet)
router.register(r'reports', ReportViewSet)


schema_view = get_swagger_view(title='Waitrss App')

app_namespace = 'waitress'

urlpatterns = [
    path('', include((router.urls, app_namespace), namespace='api',)),
    path('docs/', schema_view),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
