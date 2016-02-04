from app.viewsets import MealSessionViewSet, UserViewSet, ReportViewSet
from app import urls as app_urls
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'meal-sessions', MealSessionViewSet)
router.register(r'users', UserViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
    url(r'^', include(app_urls)),
]
