from django.db import models


class Bank5Users(models.Model):
    class Meta:
        verbose_name = "Bank of Baroda User"
        verbose_name_plural = "Bank of Baroda Users"

    accountID = models.CharField(max_length=12, verbose_name="Account ID", unique=True, null=False, blank=False)
    balance = models.IntegerField(default=0, verbose_name="Account Balance", blank=False, null=False)
    aadhaarNo = models.CharField(max_length=12, verbose_name="Aadhaar Card No.", blank=False, null=False, unique=True)
    panNo = models.CharField(max_length=12, verbose_name="PAN Card No.", blank=False, null=False)
    mobileNo = models.CharField(max_length=10, verbose_name="Mobile No.", blank=False, null=False, unique=True)
    address = models.TextField(max_length=100, verbose_name="Address", blank=False, null=False)
    emailID = models.EmailField(verbose_name="Email ID", blank=False, null=False, unique=True)
    fullName = models.CharField(max_length=40, verbose_name="Full Name", blank=False, null=False)
    apiKey = models.CharField(max_length=128, verbose_name="API Key", unique=True, blank=True, null=True)
    dCardNo = models.CharField(max_length=16, verbose_name="Debit Card Number", blank=True, null=True, unique=True)
    dCardExp = models.CharField(max_length=5, verbose_name="Debit Card Expiry", blank=True, null=True)
    dCardCVV = models.CharField(max_length=3, verbose_name="Debit Card CVV", blank=True, null=True)
    cCardNo = models.CharField(max_length=16, verbose_name="Credit Card Number", blank=True, null=True, unique=True)
    cCardExp = models.CharField(max_length=5, verbose_name="Credit Card Expiry", blank=True, null=True)
    cCardCVV = models.CharField(max_length=3, verbose_name="Credit Card CVV", blank=True, null=True)
    cCardBal = models.IntegerField(default=0, verbose_name="Credit Card Balance", blank=True, null=True)


class Bank5Transactions(models.Model):
    class Meta:
        verbose_name = "Bank of Baroda Transaction"
        verbose_name_plural = "Bank of Baroda Transactions"

    time = models.DateTimeField(verbose_name="Time", auto_now_add=True)
    transID = models.CharField(max_length=12, verbose_name="Transaction ID", blank=False, null=False, unique=True)
    senderID = models.CharField(max_length=12, verbose_name="Sender ID", null=False, blank=False)
    receiverID = models.CharField(max_length=12, verbose_name="Receiver ID", null=False, blank=False)
    amount = models.IntegerField(default=0, verbose_name="Transaction Amount", blank=False, null=False)
    description = models.CharField(max_length=20, verbose_name="Description", blank=True, null=True)
    sbankID = models.IntegerField(verbose_name="Sender Bank ID", null=False, blank=False)
    rbankID = models.IntegerField(verbose_name="Receiver Bank ID", null=False, blank=False)


class Bank5LoanOffers(models.Model):
    class Meta:
        verbose_name = "Bank of Baroda Loan Offer"
        verbose_name_plural = "Bank of Baroda Loan Offers"

    accountID = models.CharField(max_length=12, verbose_name="Account ID", null=False, blank=False)
    description = models.TextField(verbose_name="Loan Offer", blank=False, null=False)
    category = models.CharField(max_length=10, verbose_name="Category", null=False, blank=False)