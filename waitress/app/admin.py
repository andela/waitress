from django.contrib import admin

# Register your models here.
from app.models import MealService, Passphrase, SlackUser

# from django.contrib.auth.models import User


@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    search_fields = ["firstname", "lastname"]
    list_display = ("id", "firstname", "lastname", "email", "slack_id", "is_active")
    exclude = ("password", "last_login")
    readonly_fields = ("slack_id",)


@admin.register(MealService)
class MealServiceAdmin(admin.ModelAdmin):
    search_fields = ["user__firstname", "user__lastname"]
    exclude = ("date_modified",)
    list_display = ("date", "user", "breakfast", "lunch", "untapped")
    list_filter = ("date",)
    readonly_fields = ("date", "user")


@admin.register(Passphrase)
class PassphraseAdmin(admin.ModelAdmin):
    list_display = ("word",)
