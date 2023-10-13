import json
import random

from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from bank1.views import checkAccID, createTransaction


@csrf_exempt
def accountInfo(request):
    res = {"status": 500, "message": "FAILED", "response": None}

    if request.method == "GET":
        if "apiKey" in request.GET and request.GET.get("apiKey") in [_.apiKey for _ in Bank5Users.objects.all()]:
            u = Bank5Users.objects.get(apiKey=request.GET["apiKey"])
            res["status"] = 200
            res["message"] = "SUCCESS"
            res["response"] = {
                "accountID": u.accountID,
                "balance": u.balance,
                "aadhaarNo": u.aadhaarNo,
                "panNo": u.panNo,
                "mobileNo": u.mobileNo,
                "address": u.address,
                "emailID": u.emailID,
                "dCardNo": "XXXX XXXX XXXX " + u.dCardNo[-4:] if u.dCardNo else None,
                "dCardExp": u.dCardExp if u.dCardNo else None,
                "cCardNo": "XXXX XXXX XXXX " + u.cCardNo[-4:] if u.cCardNo else None,
                "cCardExp": u.cCardExp if u.cCardNo else None,
                "cCardBal": u.cCardBal if u.cCardNo else None,
            }
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    elif request.method == "POST":
        if all(list(map(lambda x: x in request.POST, ["apiKey", "emailID", "address"]))) and request.POST.get(
            "apiKey"
        ) in [_.apiKey for _ in Bank5Users.objects.all()]:
            u = Bank5Users.objects.get(apiKey=request.POST["apiKey"])
            res["status"] = 200
            res["message"] = "SUCCESS"
            u.emailID = request.POST["emailID"]
            u.address = request.POST["address"]
            u.save()
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
        if "apiKey" in request.GET and request.GET.get("apiKey") in [_.apiKey for _ in Bank5Users.objects.all()]:
            u = Bank5Users.objects.get(apiKey=request.GET["apiKey"])
            trans = Bank5Transactions.objects.filter(Q(senderID=u.accountID) | Q(receiverID=u.accountID)).order_by(
                "-time"
            )
            res["status"] = 200
            res["message"] = "SUCCESS"
            res["response"] = [
                {
                    "time": str(_.time),
                    "transID": _.transID,
                    "senderID": _.senderID,
                    "receiverID": _.receiverID,
                    "amount": _.amount,
                    "description": _.description,
                    "sbankID": _.sbankID,
                    "rbankID": _.rbankID,
                }
                for _ in trans
            ]
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    elif request.method == "POST":
        if all(
            list(map(lambda x: x in request.POST, ["apiKey", "receiverID", "amount", "rbankID"]))
        ) and request.POST.get("apiKey") in [_.apiKey for _ in Bank5Users.objects.all()]:
            u = Bank5Users.objects.get(apiKey=request.POST["apiKey"])
            if checkAccID(str(request.POST["rbankID"]), str(request.POST["receiverID"])):
                if int(request.POST["amount"]) > 0:
                    if u.balance >= int(request.POST["amount"]):
                        t = createTransaction(
                            u,
                            int(request.POST["amount"]),
                            str(request.POST["receiverID"]),
                            5,
                            int(request.POST["rbankID"]),
                            request.POST.get("description"),
                        )
                        res["status"] = 200
                        res["message"] = "Transaction Successful"
                        res["response"] = {
                            "time": str(t.time),
                            "transID": t.transID,
                            "senderID": t.senderID,
                            "receiverID": t.receiverID,
                            "amount": t.amount,
                            "description": t.description,
                        }
                    else:
                        res["status"] = 404
                        res["message"] = "Insufficient Balance"
                else:
                    res["status"] = 400
                    res["message"] = "Invalid Amount"
            else:
                res["status"] = 404
                res["message"] = "Invalid Receiver ID"
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
        if "apiKey" in request.GET and request.GET.get("apiKey") in [_.apiKey for _ in Bank5Users.objects.all()]:
            u = Bank5Users.objects.get(apiKey=request.GET["apiKey"])
            res["response"] = [
                {"category": _.category, "description": _.description}
                for _ in Bank5LoanOffers.objects.filter(accountID=u.accountID)
            ]
            res["status"] = 200
            res["message"] = "SUCCESS"
        else:
            res["status"] = 403
            res["message"] = "Invalid API Key"
    else:
        res["status"] = 400
        res["message"] = "Invalid HTTP Method"

    return HttpResponse(json.dumps(res), content_type="application/json")