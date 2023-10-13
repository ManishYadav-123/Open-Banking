from django.contrib import admin

from .models import *


class CoreUsersAdmin(admin.ModelAdmin):
    list_display = ("mobileNo", "aadhaarNo")
    search_fields = ("mobileNo", "aadhaarNo")


class CoreAPIAdmin(admin.ModelAdmin):
    list_display = ("bankName", "url")
    search_fields = ("bankName", "url")


admin.site.register(CoreUsers, CoreUsersAdmin)
admin.site.register(CoreBankAPIs, CoreAPIAdmin)
