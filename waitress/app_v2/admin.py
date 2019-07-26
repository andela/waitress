from django.contrib import admin
from django.contrib.auth.models import User


# Register your models here.
class WaitressV2AdminSite(admin.AdminSite):
    site_header = "Waitress V2 Administration"


class UserAdminSite(admin.ModelAdmin):
    search_fields = ["username", "firstname"]
    readonly_fields = ("password",)


admin_site = WaitressV2AdminSite(name="adminV2")
admin_site.register(User, UserAdminSite)
