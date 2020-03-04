from django.contrib import admin

from pantry.models import Pantry


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "user_id", "owner")
    verbose_name = "Pantry"
    verbose_name_plural = "Pantries"

    def owner(self, pantry):
        return f"{pantry.user.firstname} {pantry.user.lastname}"
