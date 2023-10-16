from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company, APIManager, Provider, Commission, CommissionType, Reports
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import uuid, requests
from .AEPSViews import Token
import random
import hmac
import base64
import hashlib
import time
import requests
import socket
from datetime import datetime
import json


def GenerateEKOSecretKey():
    # import pdb; pdb.set_trace()
    secret_key_timestamp = str(int(round(time.time()*1000)))
    key = b'd2fe1d99-6298-4af2-8cc5-d97dcf46df30'
    # dkey = key.encode('utf-8')
    dig = hmac.new(
    base64.b64encode(key), secret_key_timestamp.encode(), hashlib.sha256
    ).digest()
    secret_key = base64.b64encode(dig).decode()
    data = {"secret_key" : secret_key, "time_stamp":secret_key_timestamp}
    print(data)

    return data

def GenerateEkoSecretTimeStamp():
    secret_key_timestamp = str(int(round(time.time()*1000)))
    return secret_key_timestamp

def DMTRetailerOnBoard(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    return render(request, "money_transfer.html", {"data":pdata.eko_onboarding})

def CreateDMTRetailerOnBoard(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    if(pdata.eko_onboarding == True):
        
        mobile = user.phone
        first_name = user.name
        dob = pdata.dob
        residence_address = pdata.address


        url = f"https://staging.eko.in:25004/ekoapi/v2/customers/mobile_number:{mobile}"

        payload=f"initiator_id={initiator_id}&name={first_name}&user_code={user_code}&dob={dob}&residence_address={residence_address}&pipe=9"
        headers = {
        'developer_key': developer_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'secret-key': secret_key,
        'secret-key-timestamp': secret_time_stamp
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        return JsonResponse(response.json())
    else:
        url = f"https://staging.eko.in:25004/ekoapi/v2/customers/mobile_number:{user.phone}?initiator_id={initiator_id}&user_code={user_code}"

        payload={}
        headers = {
        'developer_key': developer_key,
        'secret-key': secret_key,
        'secret-key-timestamp': secret_time_stamp,
        'content-type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        
        return JsonResponse(response.json())

def EkoCustomerVerifyOTP(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    if(request.method == "POST"):
        otp = request.POST.get("otp")
        url = f"https://staging.eko.in:25004/ekoapi/v2/customers/verification/otp:{otp}"

        payload=f"initiator_id={initiator_id}&id_type=mobile_number&id={user.phone}&otp_ref_id=d3e00033-ebd1-5492-a631-53f0dbf00d69&user_code={user_code}&pipe=9"
        headers = {
        'developer_key': developer_key,
        'secret-key': secret_key,
        'secret-key-timestamp': secret_time_stamp,
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)
    return JsonResponse({"data":"success"})

def EkoAddReceipient(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    if(request.method == "POST"):
        mobile = request.POST.get("mobile")
        bank_id = request.POST.get("bank_id")
        name = request.POST.get("name")
        url = f"https://staging.eko.in:25004/ekoapi/v2/customers/mobile_number:{user.phone}/recipients/acc_ifsc:1711890657_KKBK0000731"

        payload=f"initiator_id={initiator_id}&recipient_mobile={mobile}&bank_id={bank_id}&recipient_type=3&recipient_name={name}&user_code={user_code}"
        headers = {
            'developer_key': developer_key,
            'secret-key': secret_key,
            'secret-key-timestamp': secret_time_stamp,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)
    return JsonResponse({"data":"success"})


def EkoGetListRecepient(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    url = f"https://staging.eko.in:25004/ekoapi/v2/customers/mobile_number:{user.phone}/recipients?initiator_id={initiator_id}&user_code={user_code}"

    payload={}
    headers = {
    'developer_key': developer_key,
    'secret-key': secret_key,
    'secret-key-timestamp': secret_time_stamp
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return JsonResponse({"data":"success"})
    


def EkoInitiateTransection(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    if(request.method == "POST"):
        recipient_id = request.POST.get("rid")
        amount = request.POST.get("amount")
        channel = request.POST.get("channel")
        state = request.POST.get("state")
        time_stamp = request.POST.get("time_stamp")
        currency = request.POST.get("currency")
        unique_ref_id = request.POST.get("unique_ref_id")
        lat_long = request.POST.get("lat_long")

        url = "https://staging.eko.in:25004/ekoapi/v2/transactions"

        payload=f"initiator_id={initiator_id}&customer_id={user.phone}&recipient_id={recipient_id}&amount={amount}&channel={channel}&state={state}&timestamp={time_stamp}&currency={currency}&latlong={lat_long}&client_ref_id={unique_ref_id}&user_code={user_code}"
        headers = {
        'developer_key': developer_key,
        'secret-key': secret_key,
        'secret-key-timestamp': secret_time_stamp,
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    return JsonResponse({"data":"message"})


## EKO AEPS Integration

def EKOMahaAgentOnboarding(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    developer_key = "becbbce45f79c6f5109f848acd540567"
    initiator_id = "9962981729"
    user_code ="20810200"
    sko_gen = GenerateEKOSecretKey()

    secret_time_stamp = sko_gen["time_stamp"]
    secret_key = sko_gen["secret_key"]
    if(request.method == "POST"):
        url = "https://staging.eko.in:25004/ekoapi/v1/user/onboard"

        payload = f"initiator_id={initiator_id}&pan_number={pdata.pan_card}&mobile={user.phone}&first_name={user.name}&last_name=S&email={user.email}&residence_address={pdata.address}&dob={pdata.dob}&shop_name={pdata.shop_name}"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'developer_key': developer_key,
            'secret-key': secret_key,
            'secret-key-timestamp': secret_time_stamp,
            'cache-control': "no-cache",
            }

        response = requests.request("PUT", url, data=payload, headers=headers)

        print(response.text)
    return JsonResponse({"data":"success"})

def EKOAEPS(request):
    return render(request, "aeps-eko.html")

def PAEPSBankList(request):
    tk = Token()
    url = "https://paysprint.in/service-api/api/v1/service/aeps/banklist/index"
    jwttoken =tk.JsonWebTokenGenerator()
    headers = {
        "accept": "application/json",
        "Token": jwttoken
    }

    response = requests.post(url, headers=headers)

    print(response.json())
    return JsonResponse({"data":response.json()})



def PAEPS_Onboardiing(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    tk = Token()
    jwttoken =tk.JsonWebTokenGenerator()
    url = "https://paysprint.in/service-api/api/v1/service/onboard/onboardnew/getonboardurl"

    payload = {
        "merchantcode": "1",
        "mobile": user.phone,
        "is_new": "1",
        "email": user.email,
        "firm": pdata.shop_name,
        "callback": "http://127.0.0.1:80000/demo"
    }
    headers = {
        "accept": "application/json",
        "Token": jwttoken,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data =  response.json()
    if(data["status"] == False):
        return JsonResponse({"redirect_url":"https://paysprint.in/"}) 

    print(response.json())
    return JsonResponse({"data":"success"})

def PAEPSDailyAuthentication(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    if(pdata.aeps_onboarding != True):
        if(request.method == "POST"):
            lat = request.POST.get("lat")
            long = request.POST.get("long")
            xml_data = request.POST.get("finger_code")
            tk = Token()
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            sub_merchant = "PYT"+ str(random.randint(000, 999))
            
            jwttoken =tk.JsonWebTokenGenerator()
            url = "https://paysprint.in/service-api/api/v1/service/aeps/kyc/Twofactorkyc/authentication"
            onboarding_data = {"accessmodetype":"APP", 
                            "adhaarnumber":pdata.aadhar_card,
                            "mobilenumber":user.phone,
                            "latitude":lat,
                            "longitude":long,
                            "referenceno":uuid.uuid4().hex[:8] ,
                            "submerchantid":sub_merchant,
                            "timestamp":str(datetime.now()),
                            "data":xml_data,
                            "ipaddress":ip_address
                            }
            print(onboarding_data)
            body_data = tk.EncryptStringToBytes(json.dumps(onboarding_data))
            payload = { "body": body_data }

            headers = {
                "accept": "application/json",
                "Token": jwttoken,
                "Authorisedkey": "NWIyMmY2YTE5NTRhZmIyNWQ3Mzc3NjdjODc2NTdjYzI=",
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=payload, headers=headers)
            rsp_data = response.json()
            print(rsp_data)
    return JsonResponse({"data":"success"}) 
