from django.contrib import admin

from .models import *


class Bank1UsersAdmin(admin.ModelAdmin):
    list_display = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance")
    search_fields = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance", "dCardNo", "cCardNo")


class Bank1TransAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "transID", "senderID", "receiverID", "amount", "description")
    search_fields = ("transID", "senderID", "receiverID")


class Bank1LoansAdmin(admin.ModelAdmin):
    list_display = ("accountID", "description")
    search_fields = ("accountID",)


admin.site.register(Bank1Users, Bank1UsersAdmin)
admin.site.register(Bank1Transactions, Bank1TransAdmin)
admin.site.register(Bank1LoanOffers, Bank1LoansAdmin)