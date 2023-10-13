from django.contrib import admin

from .models import *


class Bank4UsersAdmin(admin.ModelAdmin):
    list_display = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance")
    search_fields = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance", "dCardNo", "cCardNo")


class Bank4TransAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "transID", "senderID", "receiverID", "amount", "description")
    search_fields = ("transID", "senderID", "receiverID")


class Bank4LoansAdmin(admin.ModelAdmin):
    list_display = ("accountID", "description")
    search_fields = ("accountID",)


admin.site.register(Bank4Users, Bank4UsersAdmin)
admin.site.register(Bank4Transactions, Bank4TransAdmin)
admin.site.register(Bank4LoanOffers, Bank4LoansAdmin)