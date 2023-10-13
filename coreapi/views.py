import os
import json
import string
import random
import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from bank1.models import *
from bank2.models import *
from bank3.models import *
from bank4.models import *
from bank5.models import *


@csrf_exempt
def authAadhaar(request):
    res = {"status": 500, "message": "FAILED", "response": None}

    if request.method == "GET":
        if "aadhaarNo" in request.GET:
            u = CoreUsers.objects.get(aadhaarNo=request.GET["aadhaarNo"])
            u.generateOTP()
            res["status"] = 200
            res["message"] = "OTP sent to your registered mobile number"
        else:
            res["message"] = "Invalid Parameters"
    elif request.method == "POST":
        if "aadhaarNo" in request.POST and "otp" in request.POST:
            u = CoreUsers.objects.get(aadhaarNo=request.POST["aadhaarNo"])
            if request.POST["otp"] == u.otp:
                res["status"] = 200
                res["message"] = "Auth Success"
                u.apiKey = hashlib.blake2b(("BANK" + str(time.time())).encode()).hexdigest()
                u.save()
                try:
                    u2 = Bank1Users.objects.get(mobileNo=u.mobileNo)
                    u2.apiKey = u.apiKey
                    u2.save()
                except:
                    pass
                try:
                    u2 = Bank2Users.objects.get(mobileNo=u.mobileNo)
                    u2.apiKey = u.apiKey
                    u2.save()
                except:
                    pass
                try:
                    u2 = Bank3Users.objects.get(mobileNo=u.mobileNo)
                    u2.apiKey = u.apiKey
                    u2.save()
                except:
                    pass
                try:
                    u2 = Bank4Users.objects.get(mobileNo=u.mobileNo)
                    u2.apiKey = u.apiKey
                    u2.save()
                except:
                    pass
                try:
                    u2 = Bank5Users.objects.get(mobileNo=u.mobileNo)
                    u2.apiKey = u.apiKey
                    u2.save()
                except:
                    pass
                u.otp = str(random.randint(100000, 999999))
                u.save()
                res["response"] = u.apiKey
            else:
                res["status"] = 404
                res["message"] = "Invalid OTP"
        else:
            res["message"] = "Invalid Parameters"
    else:
        res["status"] = 400
        res["message"] = "Invalid HTTP Method"

    return HttpResponse(json.dumps(res), content_type="application/json")


@csrf_exempt
def accountInfo(request):
    res = {"status": 500, "message": "FAILED", "response": None}

    if request.method == "GET":
        if "apiKey" in request.GET and request.GET.get("apiKey") in [_.apiKey for _ in CoreUsers.objects.all()]:
            res["status"] = 200
            res["message"] = "SUCCESS"
            res["response"] = []
            for i in range(1, 6):
                res["response"].append(
                    {
                        "bankID": i,
                        "data": json.loads(
                            requests.get(
                                CoreBankAPIs.objects.get(id=i).url + "account", params={"apiKey": request.GET["apiKey"]}
                            ).text
                        )["response"],
                    }
                )
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    elif request.method == "POST":
        if all(list(map(lambda x: x in request.POST, ["apiKey", "address", "emailID", "bankID"]))) and request.POST.get(
            "apiKey"
        ) in [_.apiKey for _ in CoreUsers.objects.all()]:
            res = json.loads(
                requests.post(
                    CoreBankAPIs.objects.get(id=int(request.POST["bankID"])).url + "account",
                    data={
                        "apiKey": request.POST["apiKey"],
                        "address": request.POST["address"],
                        "emailID": request.POST["emailID"],
                    },
                ).text
            )
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    else:
        res["status"] = 400
        res["message"] = "Invalid HTTP Method"

    return HttpResponse(json.dumps(res), content_type="application/json")


@csrf_exempt
def accTransaction(request):
    res = {"status": 500, "message": "FAILED", "response": None}

    if request.method == "GET":
        if all(list(map(lambda x: x in request.GET, ["apiKey", "bankID"]))) and request.GET.get("apiKey") in [
            _.apiKey for _ in CoreUsers.objects.all()
        ]:
            res = json.loads(
                requests.get(
                    CoreBankAPIs.objects.get(id=int(request.GET["bankID"])).url + "transactions",
                    params={"apiKey": request.GET["apiKey"]},
                ).text
            )
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    elif request.method == "POST":
        if all(
            list(map(lambda x: x in request.POST, ["apiKey", "receiverID", "amount", "rbankID", "sbankID"]))
        ) and request.POST.get("apiKey") in [_.apiKey for _ in CoreUsers.objects.all()]:
            res = json.loads(
                requests.post(
                    CoreBankAPIs.objects.get(id=int(request.POST["sbankID"])).url + "transactions",
                    data={
                        "apiKey": request.POST["apiKey"],
                        "receiverID": request.POST["receiverID"],
                        "amount": request.POST["amount"],
                        "rbankID": request.POST["rbankID"],
                        "description": request.POST.get("description"),
                    },
                ).text
            )
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    else:
        res["status"] = 400
        res["message"] = "Invalid HTTP Method"

    return HttpResponse(json.dumps(res), content_type="application/json")


@csrf_exempt
def loanOffers(request):
    res = {"status": 500, "message": "FAILED", "response": None}

    if request.method == "GET":
        if "apiKey" in request.GET and request.GET.get("apiKey") in [_.apiKey for _ in CoreUsers.objects.all()]:
            res["status"] = 200
            res["message"] = "SUCCESS"
            res["response"] = []
            for i in range(1, 6):
                res["response"].append(
                    {
                        "bankID": i,
                        "data": json.loads(
                            requests.get(
                                CoreBankAPIs.objects.get(id=i).url + "loans",
                                params={"apiKey": request.GET["apiKey"], "category": request.GET["category"]}
                                if request.GET.get("category")
                                else {"apiKey": request.GET["apiKey"]},
                            ).text
                        )["response"],
                    }
                )
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    else:
        res["status"] = 400
        res["message"] = "Invalid HTTP Method"

    return HttpResponse(json.dumps(res), content_type="application/json")


def loginPage(request):
    return render(request, "login.html")


def transPage(request):
    return render(request, "trans.html")


def dashPage(request):
    return render(request, "accounts.html")


def indexPage(request):
    return render(request, "index.html")


def transferPage(request):
    return render(request, "transfer.html")


def loansPage(request):
    return render(request, "getloans.html")


def dummy():
    aadhaarNo = str(random.randint(10 ** 11, (10 ** 12) - 1))
    mobileNo = str(random.randint(10 ** 9, (10 ** 10) - 1))
    panNo = (
        "".join(random.choices(string.ascii_uppercase, k=5))
        + str(random.randint(10 ** 3, (10 ** 4) - 1))
        + random.choice(string.ascii_uppercase)
    )
    emailID = "".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com"
    fullName = "Test Kumar"

    print("-------------------------")
    print("[!] Test Account Details")
    print("-------------------------")
    print("[+] Full Name:", fullName)
    print("[+] Aadhaar Card No.:", aadhaarNo)
    print("[+] Mobile No.:", mobileNo)
    print("[+] Email ID:", emailID)
    print("[+] PAN Card No.:", panNo)
    print("-------------------------")

    print("\n[!] Creating Test Account in Banks .. ", end="")
    accountID1 = str(random.randint(10 ** 11, (10 ** 12) - 1))
    accountID2 = str(random.randint(10 ** 11, (10 ** 12) - 1))
    accountID5 = str(random.randint(10 ** 11, (10 ** 12) - 1))
    Bank1Users(
        accountID=accountID1,
        balance=random.randint(10 ** 3, (10 ** 5) - 1),
        aadhaarNo=aadhaarNo,
        panNo=panNo,
        mobileNo=mobileNo,
        fullName=fullName,
        address="Near ABCD Mall, Mumbai, India",
        emailID=emailID,
        dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
        dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
        dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
        cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
        cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
        cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
        cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
    ).save()
    Bank2Users(
        accountID=accountID2,
        balance=random.randint(10 ** 3, (10 ** 5) - 1),
        aadhaarNo=aadhaarNo,
        panNo=panNo,
        mobileNo=mobileNo,
        fullName=fullName,
        address="Near ABCD Mall, Mumbai, India",
        emailID=emailID,
        cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
        cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
        cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
        cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
    ).save()
    Bank5Users(
        accountID=accountID5,
        balance=random.randint(10 ** 3, (10 ** 5) - 1),
        aadhaarNo=aadhaarNo,
        panNo=panNo,
        mobileNo=mobileNo,
        fullName=fullName,
        address="Near ABCD Mall, Mumbai, India",
        emailID=emailID,
    ).save()
    print("[DONE]")

    print("[!] Creating 3 Dummy Accounts in every Bank .. ", end="")
    for _ in range(3):
        Bank1Users(
            accountID=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            balance=random.randint(10 ** 3, (10 ** 5) - 1),
            aadhaarNo=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            panNo="".join(random.choices(string.ascii_uppercase, k=5))
            + str(random.randint(10 ** 3, (10 ** 4) - 1))
            + random.choice(string.ascii_uppercase),
            mobileNo=str(random.randint(10 ** 9, (10 ** 10) - 1)),
            fullName="".join(random.choices(string.ascii_uppercase, k=6)).capitalize() + " Kumar",
            address="Near ABCD Mall, Mumbai, India",
            emailID="".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com",
            dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
        ).save()
        Bank2Users(
            accountID=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            balance=random.randint(10 ** 3, (10 ** 5) - 1),
            aadhaarNo=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            panNo="".join(random.choices(string.ascii_uppercase, k=5))
            + str(random.randint(10 ** 3, (10 ** 4) - 1))
            + random.choice(string.ascii_uppercase),
            mobileNo=str(random.randint(10 ** 9, (10 ** 10) - 1)),
            fullName="".join(random.choices(string.ascii_uppercase, k=6)).capitalize() + " Kumar",
            address="Near ABCD Mall, Mumbai, India",
            emailID="".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com",
            dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
        ).save()
        Bank3Users(
            accountID=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            balance=random.randint(10 ** 3, (10 ** 5) - 1),
            aadhaarNo=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            panNo="".join(random.choices(string.ascii_uppercase, k=5))
            + str(random.randint(10 ** 3, (10 ** 4) - 1))
            + random.choice(string.ascii_uppercase),
            mobileNo=str(random.randint(10 ** 9, (10 ** 10) - 1)),
            fullName="".join(random.choices(string.ascii_uppercase, k=6)).capitalize() + " Kumar",
            address="Near ABCD Mall, Mumbai, India",
            emailID="".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com",
            dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
        ).save()
        Bank4Users(
            accountID=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            balance=random.randint(10 ** 3, (10 ** 5) - 1),
            aadhaarNo=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            panNo="".join(random.choices(string.ascii_uppercase, k=5))
            + str(random.randint(10 ** 3, (10 ** 4) - 1))
            + random.choice(string.ascii_uppercase),
            mobileNo=str(random.randint(10 ** 9, (10 ** 10) - 1)),
            fullName="".join(random.choices(string.ascii_uppercase, k=6)).capitalize() + " Kumar",
            address="Near ABCD Mall, Mumbai, India",
            emailID="".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com",
            dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
        ).save()
        Bank5Users(
            accountID=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            balance=random.randint(10 ** 3, (10 ** 5) - 1),
            aadhaarNo=str(random.randint(10 ** 11, (10 ** 12) - 1)),
            panNo="".join(random.choices(string.ascii_uppercase, k=5))
            + str(random.randint(10 ** 3, (10 ** 4) - 1))
            + random.choice(string.ascii_uppercase),
            mobileNo=str(random.randint(10 ** 9, (10 ** 10) - 1)),
            fullName="".join(random.choices(string.ascii_uppercase, k=6)).capitalize() + " Kumar",
            address="Near ABCD Mall, Mumbai, India",
            emailID="".join(random.choices(string.ascii_uppercase, k=6)) + "@gmail.com",
            dCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            dCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            dCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardNo=str(random.randint(10 ** 15, (10 ** 16) - 1)),
            cCardExp=str(random.randint(1, 12)) + "/" + str(random.randint(21, 28)),
            cCardCVV=str(random.randint(10 ** 2, (10 ** 3) - 1)),
            cCardBal=random.randint(10 ** 3, (10 ** 5) - 1),
        ).save()
    print("[DONE]")

    print("[!] Creating Dummy Transactions for Test Account .. ", end="")
    for _ in range(15):
        ch = random.choice([1, 2, 5])
        if ch == 1:
            Bank1Transactions(
                transID=random.randint(10 ** 9, (10 ** 10) - 1),
                senderID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 == 0 else accountID1,
                receiverID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 != 0 else accountID1,
                amount=str(random.randint(10, (10 ** 3) - 1)),
                sbankID=random.choice([2, 3, 4, 5]) if _ % 2 == 0 else 1,
                rbankID=random.choice([2, 3, 4, 5]) if _ % 2 != 0 else 1,
            ).save()
        elif ch == 2:
            Bank2Transactions(
                transID=random.randint(10 ** 9, (10 ** 10) - 1),
                senderID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 == 0 else accountID2,
                receiverID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 != 0 else accountID2,
                amount=str(random.randint(10, (10 ** 3) - 1)),
                sbankID=random.choice([1, 3, 4, 5]) if _ % 2 == 0 else 2,
                rbankID=random.choice([1, 3, 4, 5]) if _ % 2 != 0 else 2,
            ).save()
        elif ch == 5:
            Bank5Transactions(
                transID=random.randint(10 ** 9, (10 ** 10) - 1),
                senderID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 == 0 else accountID5,
                receiverID=str(random.randint(10 ** 11, (10 ** 12) - 1)) if _ % 2 != 0 else accountID5,
                amount=str(random.randint(10, (10 ** 3) - 1)),
                sbankID=random.choice([1, 3, 4, 2]) if _ % 2 == 0 else 5,
                rbankID=random.choice([1, 3, 4, 2]) if _ % 2 != 0 else 5,
            ).save()
    print("[DONE]")

    print("[!] Creating Loan Offers for Test Account .. ", end="")
    Bank1LoanOffers(accountID=accountID1, category="personal", description="TEST").save()
    Bank1LoanOffers(accountID=accountID1, category="personal", description="TEST").save()
    Bank1LoanOffers(accountID=accountID1, category="home", description="TEST").save()
    Bank1LoanOffers(accountID=accountID1, category="education", description="TEST").save()
    Bank2LoanOffers(accountID=accountID2, category="home", description="TEST").save()
    Bank2LoanOffers(accountID=accountID2, category="education", description="TEST").save()
    Bank5LoanOffers(accountID=accountID5, category="education", description="TEST").save()
    Bank5LoanOffers(accountID=accountID5, category="personal", description="TEST").save()
    Bank5LoanOffers(accountID=accountID5, category="home", description="TEST").save()
    print("[DONE]")

    print("[!] Creating Test Account in Core API .. ", end="")
    CoreUsers(aadhaarNo=aadhaarNo, mobileNo=mobileNo, fullName=fullName).save()
    print("[DONE]")

    print("[!] Configuring Banks with Core API .. ", end="")
    CoreBankAPIs(bankName="State Bank of India", url="http://127.0.0.1:8000/bank1/api/v1/").save()
    CoreBankAPIs(bankName="Punjab National Bank", url="http://127.0.0.1:8000/bank2/api/v1/").save()
    CoreBankAPIs(bankName="Union Bank of India", url="http://127.0.0.1:8000/bank3/api/v1/").save()
    CoreBankAPIs(bankName="Canara Bank", url="http://127.0.0.1:8000/bank4/api/v1/").save()
    CoreBankAPIs(bankName="Bank of Baroda", url="http://127.0.0.1:8000/bank5/api/v1/").save()
    print("[DONE]")