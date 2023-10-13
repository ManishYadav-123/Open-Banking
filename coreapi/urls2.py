from django.urls import path

from .views import *

urlpatterns = [
    path("", indexPage),
    path("login", loginPage),
    path("dashboard", dashPage),
    path("loans", loansPage),
    path("transactions", transPage),
    path("transfer", transferPage),
]
