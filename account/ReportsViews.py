from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company, APIManager, Provider, Commission, CommissionType, Reports
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import uuid, requests
from .AEPSViews import Token
import random

@login_required(login_url='login')
def RechargeReport(request):
    
    return render(request, "recharge_reports.html")

def GetRechargeReportsData(request):
    if(request.method == "GET"):
        recharge_data = []
        user = request.user
        reports_data = Reports.objects.filter(user_id = user,  product="recharge")
        
        for state in reports_data:
            # print(state)
            pdata = Provider.objects.get(id=state.provider.id)
            rep_data = {"id":state.id,"txn_id":state.txn_id,"operator":pdata.name, "product":state.product, "number":state.number,"amount":state.amount,"created_at":state.created_at, "status":state.status, "commission":state.r_profit, "tds":state.tds, 
            "order_id":state.txn_id
            }
            # print(rep_data)
            recharge_data.append(rep_data)
    return JsonResponse({"data":recharge_data})

def ShowReceiptRecharge(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        r_data = Reports.objects.get(id=id)
        p_data = Provider.objects.get(id = r_data.provider.id)
        report_data = {"created_at":r_data.created_at, "txn_nu":r_data.api_txn_id, "operator":p_data.name,"product":r_data.product, "status":r_data.status, "customer":r_data.number, "amount":r_data.amount , "order":r_data.txn_id }
    return JsonResponse({"data":report_data, "mtype":"success"})