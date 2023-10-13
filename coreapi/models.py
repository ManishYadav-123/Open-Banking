import time
import random
import hashlib

from django.db import models
from bank1.models import Bank1Users
from bank2.models import Bank2Users
from bank3.models import Bank3Users
from bank4.models import Bank4Users
from bank5.models import Bank5Users


class CoreUsers(models.Model):
    class Meta:
        verbose_name = "Core User"
        verbose_name_plural = "Core Users"

    aadhaarNo = models.CharField(max_length=12, verbose_name="Aadhaar Card No.", blank=False, null=False)
    mobileNo = models.CharField(max_length=10, verbose_name="Mobile No.", blank=False, null=False, unique=True)
    fullName = models.CharField(max_length=40, verbose_name="Full Name", blank=False, null=False)
    apiKey = models.CharField(max_length=128, verbose_name="API Key", unique=True, blank=True, null=True)
    otp = models.CharField(max_length=6, verbose_name="OTP", blank=True, null=True)

    def generateOTP(self):
        self.otp = str(random.randint(100000, 999999))
        print("[!] New OTP generated: " + self.otp)
        self.save()


class CoreBankAPIs(models.Model):
    class Meta:
        verbose_name = "Core API"
        verbose_name_plural = "Core APIs"

    bankName = models.CharField(max_length=20, verbose_name="Bank Name", blank=False, null=False, unique=True)
    url = models.URLField(verbose_name="API URL", blank=False, null=False, unique=True)