"""URL Definition for Waitress V2"""
from django.conf.urls import url
from django.urls import path

from app_v2.admin import admin_site
from app_v2.views import (
    login_handler,
    dashboard,
    signout,
    fetch_users,
    refresh_slack_users,
    add_guest,
    retrieve_user
)


urlpatterns = [
    path("", login_handler, name="login"),
    path("dashboard", dashboard, name="dashboard"),
    path("admin", admin_site.urls),
    path("signout", signout, name="signout"),
    path("fetch_users", fetch_users),
    path("refresh_users", refresh_slack_users),
    path("add_guest", add_guest),
    path("retrieve_user/<str:firstname>", retrieve_user)
]
