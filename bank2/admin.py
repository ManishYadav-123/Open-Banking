from django.contrib import admin

from .models import *


class Bank2UsersAdmin(admin.ModelAdmin):
    list_display = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance")
    search_fields = ("accountID", "mobileNo", "emailID", "panNo", "aadhaarNo", "balance", "dCardNo", "cCardNo")


class Bank2TransAdmin(admin.ModelAdmin):
    readonly_fields = ("time",)
    list_display = ("time", "transID", "senderID", "receiverID", "amount", "description")
    search_fields = ("transID", "senderID", "receiverID")


class Bank2LoansAdmin(admin.ModelAdmin):
    list_display = ("accountID", "description")
    search_fields = ("accountID",)


admin.site.register(Bank2Users, Bank2UsersAdmin)
admin.site.register(Bank2Transactions, Bank2TransAdmin)
admin.site.register(Bank2LoanOffers, Bank2LoansAdmin)