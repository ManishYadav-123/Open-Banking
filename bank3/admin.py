from django.contrib import admin

from .models import *


class Bank3UsersAdmin(admin.ModelAdmin):
    list_display = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance")
    search_fields = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance", "dCardNo", "cCardNo")


class Bank3TransAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "transID", "senderID", "receiverID", "amount", "description")
    search_fields = ("transID", "senderID", "receiverID")


class Bank3LoansAdmin(admin.ModelAdmin):
    list_display = ("accountID", "description")
    search_fields = ("accountID",)


admin.site.register(Bank3Users, Bank3UsersAdmin)
admin.site.register(Bank3Transactions, Bank3TransAdmin)
admin.site.register(Bank3LoanOffers, Bank3LoansAdmin)