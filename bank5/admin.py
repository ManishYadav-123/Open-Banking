from django.contrib import admin

from .models import *


class Bank5UsersAdmin(admin.ModelAdmin):
    list_display = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance")
    search_fields = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance", "dCardNo", "cCardNo")


class Bank5TransAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "transID", "senderID", "receiverID", "amount", "description")
    search_fields = ("transID", "senderID", "receiverID")


class Bank5LoansAdmin(admin.ModelAdmin):
    list_display = ("accountID", "description")
    search_fields = ("accountID",)


admin.site.register(Bank5Users, Bank5UsersAdmin)
admin.site.register(Bank5Transactions, Bank5TransAdmin)
admin.site.register(Bank5LoanOffers, Bank5LoansAdmin)