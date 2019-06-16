from django.contrib import admin

# Register your models here.
from app.models import SlackUser, MealService, Passphrase
from django.contrib.auth.models import User


class WaitressAdminSite(admin.AdminSite):
    site_header = 'Waitress Administration'


class UserAdminSite(admin.ModelAdmin):
    search_fields = ['username', 'firstname']
    readonly_fields = ('password',)


class SlackUserAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname']
    list_display = ('id', 'firstname', 'lastname', 'email', 'slack_id', 'isActive')
    exclude = ('password', 'last_login')
    readonly_fields = ('slack_id',)


class MealServiceAdmin(admin.ModelAdmin):
    search_fields = ['user__firstname', 'user__lastname']
    exclude = ('date_modified',)
    list_display = ('date', 'user', 'breakfast', 'lunch', 'untapped')
    list_filter = ('date',)
    readonly_fields = ('date', 'user')


class PassphraseAdmin(admin.ModelAdmin):
    list_display = ('word',)

admin_site = WaitressAdminSite(name='admin')
admin_site.register(User, UserAdminSite)
admin_site.register(SlackUser, SlackUserAdmin)
admin_site.register(MealService, MealServiceAdmin)
admin_site.register(Passphrase, PassphraseAdmin)
