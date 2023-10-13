from django.urls import path

from .views import *

urlpatterns = [
    path("auth", authAadhaar),
    path("account", accountInfo),
    path("transactions", accTransaction),
    path("loans", loanOffers),
]
