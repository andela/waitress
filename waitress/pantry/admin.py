from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from pantry.models import Pantry

class PantryAdminSite(admin.AdminSite):
  site_header: "Pantry Administration"


admin_site = PantryAdminSite(name="admin")
