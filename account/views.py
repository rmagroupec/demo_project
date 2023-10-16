from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company, APIManager, Provider, Commission, CommissionType, Reports, LoadWalletRequest
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import uuid, requests
from .AEPSViews import Token
import random
from datetime import datetime
import socket
import json
from geopy.geocoders import Nominatim


# Create your views here.
@login_required(login_url='login')
def index(request):
    user = request.user
    if user.role.id == 3:
        return render(request,'dashboard.html')
    else:
        return render(request,'index.html')

@login_required(login_url='login')
def superDistibuter(request):
    return render(request,'super_distibuter.html')

def registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        print(name, email, phone, password, confirm_password, role)
        checkpoint = password_check(password)
        if checkpoint == 1:
            return render(request,"register.html", {"message":"Password must contain atleast one capital alphbat"})
        if checkpoint == 2:
            return render(request,"register.html", {"message":"Password must contain atleast one digit"})
        if checkpoint == 3:
            return render(request,"register.html", {"message":"Password must contains one special character like @, $,#,&"})
        user_check_obj = Account.objects.filter(email=email).count()
        if user_check_obj != 0:
            return render(request,"register.html", {"message":'User Already Exists!'})

        if password == confirm_password:
            role = Role.objects.get(id = role)
            user = Account.objects.create_user(username=phone, name=name, email=email, phone=phone, password=password, role=role)
            UserProfile.objects.create(user=user)
            auth.login(request, user)
            return redirect(index)
        else:
            return render(request,"register.html", {"message":"Password and confirm password Does not match"})
    return render(request,"register.html")

def login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        usercheck = Account.objects.filter(phone__iexact=phone).count()
        if usercheck == 0:
            return render(request,"register.html", {"message":"Please enter valid email or password!"})
        user = auth.authenticate(request, username=phone, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(index)  # Redirect to the user's profile page or any other desired page
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    return render(request,"login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(index)

@login_required(login_url='login')
def changePassword(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        email = request.user.email
        if len(new_password) < 4:
            return render(request, 'login.html', {'error_message': 'enter password of minimun 4 digits'})

        checkpoint = password_check(new_password)
        if checkpoint == 1:
            return render(request,"register.html", {"message":"Password must contain atleast one capital alphbat"})
        if checkpoint == 2:
            return render(request,"register.html", {"message":"Password must contain atleast one digit"})
        if checkpoint == 3:
            return render(request,"register.html", {"message":"Password must contains one special character like @, $,#,&"})
        
        if new_password != confirm_new_password:
            return render(request,"register.html", {"message":"password and confirmpassword doesnot match"})
        userdata = Account.objects.get(email=email)
        if userdata.check_password(new_password):
            return render(request,"register.html", {"message":"new password already exists"})
        if userdata.check_password(old_password):
            userdata.password = new_password
            userdata.save()
            return redirect(index)
        else:
            return render(request,"register.html", {"message":"wrong current password"})
    return render(request,"login.html")

@login_required(login_url='login')
def whitelabel(request):
    role = Role.objects.get(name="White Label")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "White Label"})

@login_required(login_url='login')
def superDistributer(request):
    role = Role.objects.get(name="Super Distributer")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "Super Distributer"})

@login_required(login_url='login')
def Distributer(request):
    role = Role.objects.get(name="Distributer")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "Distributer"})

@login_required(login_url='login')
def Retailer(request):
    role = Role.objects.get(name="Retailer")
    data = Account.objects.filter(role = role)
    return render(request, 'whitelabel.html', {"data":data, "name" : "Retailer"}) 

# Scheme Manager
@login_required(login_url='login')
def SchemeManager(request):
    message= ""
    mtype=""
    scheme_data = Scheme.objects.all()
    
    com_data = CommissionType.objects.all()
    return render(request, "scheme_manager.html", {"data" : scheme_data, "pdata":com_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def GetProviderDataBYID(request):
    data = []
    if(request.method == "POST"):
        com_id = request.POST.get("com_id")
        commission = CommissionType.objects.get(id=com_id)
        print(commission)
    provider_data = Provider.objects.filter(com_type= commission) 
    for state in provider_data:
        commission = Commission.objects.filter(operator_id= state.id)
        if commission.count() >= 1:
            for cdata in commission:
                my_data = {"name":state.name, "id":state.id, "whitelabel":cdata.white_label, "super_dist":cdata.super_distributor, "distributor":cdata.distributor, "retailer":cdata.retailer, "type":cdata.type}
        else:
            my_data = {"name":state.name, "id":state.id, "whitelabel":0.0, "super_dist":0.0, "distributor":0.0, "retailer":0.0, "type":0.0}   
        data.append(my_data)
    return JsonResponse({"pdata":data})

@login_required(login_url='login')
def AddScheme(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        id = request.POST.get("sid")
        if(id == ''):
            try:
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                Scheme.objects.create(name=name, type=type1, status=status)
                message= "Added Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
        else:
            try:
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                scheme = Scheme.objects.get(id = id)
                scheme.name = name
                scheme.type = type1
                scheme.status = status
                scheme.save()
                message= "Updated Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})

@login_required(login_url='login')
def DeleteScheme(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            data.delete()
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
        # scheme_data = Scheme.objects.all()
        # return render(request, "scheme_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def editScheme(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            scheme_data = {"id":data.id, "name":data.name, "type":data.type, "status":data.status }
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message, 'data':scheme_data})    


## Commission type 
@login_required(login_url='login')
def CommissionTypeManager(request):
    message= ""
    mtype=""
    scheme_data = CommissionType.objects.all()
    return render(request, "commission_type_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def AddCommissionType(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        id = request.POST.get("sid")
        print(id, type(id))
        if(id == ''):
            try:
                print("Inside post")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                CommissionType.objects.create(name=name, type=type1, status=status)
                message= "Added Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
        else:
            try:
                print("Inside edit")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                scheme = CommissionType.objects.get(id = id)
                scheme.name = name
                scheme.type = type1
                scheme.status = status
                scheme.save()
                message= "Updated Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})

@login_required(login_url='login')
def DeleteCommssionType(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = CommissionType.objects.get(pk=id)
            data.delete()
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
        # scheme_data = Scheme.objects.all()
        # return render(request, "scheme_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def editCommissionType(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            scheme_data = {"id":data.id, "name":data.name, "type":data.type, "status":data.status }
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message, 'data':scheme_data})    



## API Manager
@login_required(login_url='login')
def apiManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            name = request.POST.get("product_name")
            sort_name = request.POST.get("sort_name")
            url = request.POST.get("url")
            status = request.POST.get("status")
            api_key = request.POST.get("api_key")
            username = request.POST.get("username")
            password = request.POST.get("password")
            optional = request.POST.get("optional")
            code = request.POST.get("code")
            type = request.POST.get("type")
            APIManager.objects.create(product_name=name, sort_name=sort_name, url=url, status=status, api_key=api_key, username=username, password=password, optional=optional, code=code, type=type)
            message= "Added Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    
    scheme_data = APIManager.objects.all()
    return render(request, "api.html", {"data" : scheme_data, "message": message, "mtype":mtype})

# Role Manager
@login_required(login_url='login')
def roleManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            name = request.POST.get("role_name")
            Role.objects.create(name=name)
            message= "Added Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    role_data = Role.objects.all()
    return render(request, "role.html", {"data" : role_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def company(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            company_name = request.POST.get("company_name")
            sort_name = request.POST.get("sort_name")
            website = request.POST.get("website")
            logo = request.FILES.get("image")
            status = request.POST.get("status")
            sender_id = request.POST.get("sender_id")
            sms_user_id = request.POST.get("sms_user_id")
            sms_password = request.POST.get("sms_password")
            sms_uti = request.POST.get("sms_uti")
            smtp_url = request.POST.get("smtp_url")
            smtp_user_name = request.POST.get("smtp_user_name")
            smtp_password = request.POST.get("smtp_password")
            smtp_port = request.POST.get("smtp_port")
            Company.objects.create(company_name = company_name, sort_name = sort_name, website = website, logo = logo, status = status, sender_id = sender_id, sms_user_id = sms_user_id, sms_password = sms_password, sms_uti = sms_uti, smtp_url = smtp_url, smtp_user_name = smtp_user_name, smtp_password = smtp_password, smtp_port = smtp_port)
            message= "Added Successfully"
            mtype="success"
        except :
            message= "Something went wrong.."
            mtype="failed"
    company = Company.objects.all()
    return render(request, "company.html", {"data" : company, "message": message, "mtype":mtype})
    api_data = APIManager.objects.all()
    return render(request, "api.html", {"data" : api_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def ProviderManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST') and request.FILES['logo']:
        # try:
        name = request.POST.get("name")
        re_1 = request.POST.get("re_1")
        re_2 = request.POST.get("re_2")
        re_3 = request.POST.get("re_3")
        re_4 = request.POST.get("re_4")
        api_id = request.POST.get("api_id")
        type = request.POST.get("type")
        status = request.POST.get("status")
        logo = request.FILES['logo']
        fss = FileSystemStorage()
        file = fss.save(logo.name, logo)
        file_url = fss.url(file)
        com_type = request.POST.get("com_type")
        commission = CommissionType.objects.get(id=com_type)
        api = APIManager.objects.get(id=api_id)
        is_mandatory = True
        Provider.objects.create(name=name, type=type,com_type=commission, status=status, logo=file_url, is_mandatory=is_mandatory, api_id=api,re_1=re_1, re_2=re_2, re_3=re_3, re_4=re_4)
        message= "Added Successfully"
        mtype="success"
        # except:
        #     message= "Something went wrong.."
        #     mtype="failed"
    api_data = APIManager.objects.all()
    com_data = CommissionType.objects.all()

    scheme_data = Provider.objects.all()
    return render(request, "provider.html", {"data" : scheme_data,"apidata":api_data,"com_data":com_data, "message": message, "mtype":mtype})

@login_required(login_url='login')
def AddCommission(request):
    mtype = ""
    message = ""
    if(request.method == 'POST'):
        com_type_id = request.POST.get("com_id")
        scheme_id = request.POST.get("scheme_id")
        ids = request.POST.get("ids")
        types = request.POST.get("type")
        whitelabel = request.POST.get("whitelabel")
        super_dist = request.POST.get("super_dist")
        distributor = request.POST.get("distributor")
        retailer = request.POST.get("retailer")
        commission = CommissionType.objects.get(id=com_type_id)
        scheme = Scheme.objects.get(id=scheme_id)
        
        for id, type, wl, sd, dn, rt in zip(ids.split(','), types.split(','), whitelabel.split(','), super_dist.split(','), distributor.split(','), retailer.split(',')):
            print(id, type, wl, sd, dn, rt)
            operator = Provider.objects.get(id=id)
            Commission.objects.create(com_type_id=commission,operator_id=operator, scheme_id=scheme, type=type,  white_label=wl, super_distributor=sd, distributor=dn, retailer=rt)
            message= "Added Successfully"
            mtype="success"
            # pass
        # data = parse_qs(form_data, output)
        print(ids, types, whitelabel, super_dist, distributor, retailer)        
    return JsonResponse({'mtype':mtype, 'message':message})

@login_required(login_url='login')
def GetCommissionBySchemeAndCType(request):
    if(request.method == "POST"):
        com_type_id = request.POST.get('com_id')
        # scheme_id = request.POST.get('scheme_id')
        comm_data = Commission.objects.all()
        print(comm_data)
        cdata =[]
        for data in comm_data:
            com_data = { "com_type_id":data.com_type_id,  "type":data.type, "white_label":data.white_label, "super_distributor":data.super_distributor, "distributor":data.distributor, "retailer":data.retailer }
            cdata.append(com_data)
    return JsonResponse({"data":cdata})           

@login_required(login_url='login')
def ProfileManager(request, id):
    user = Account.objects.get(id = id)
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'profile.html', {"profile_data":user_profile})


@login_required(login_url='login')
def UserProfileManager(request):
    lat = ""
    long = ""
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    role = Role.objects.all()
    distributer = Account.objects.filter(role=4)
    
    return render(request, 'user-profile.html', {"profile_data":user_profile, "ip_address":ip_address, "lat":lat, "long":long, "location":"", "role":role, "distr":distributer})
def FetchCurrentLocation(request):
    if(request.method == "POST"):
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        geoLoc = Nominatim(user_agent="GetLoc")
        locname = geoLoc.reverse(f"{lat}, {long}")
    return JsonResponse({"location":locname.address, "lat":lat, "long":long})

## change password 
@login_required(login_url='login')
def ChangePassword(request):
    mtype =""
    message=""
    try:
        if(request.method == "POST"):
            password = request.POST.get("password")
            user = request.user
            user = Account.objects.get(id=user.id)
            user.password = password
            user.save()
            mtype="success"
            message="Password Changes Successfully"
    except:
        mtype="failed"
        message="Something went wrong!...."
    return JsonResponse({"mtype":mtype, "message":message})

## mobile recharge process
@login_required(login_url='login')
def MobileRecharge(request):
    rdata = Provider.objects.filter(type="recharge")
    user = request.user
    reports_data = Reports.objects.filter(user_id = user,  product="recharge").order_by('-id')[:8]
    return render(request, "recharge.html", {"rdata":rdata, "reports_data":reports_data})

@login_required(login_url='login')
def MobileRechargeRequest(request):
    if(request.method == "POST"):
        # import pdb; pdb.set_trace()
        operator = request.POST.get("operator")
        number = request.POST.get("number")
        amount = request.POST.get("amount")
        pin = request.POST.get("pin")
        user = request.POST.get("pin")
        try:
            pdata = Provider.objects.get(name=operator)
        except:
            return JsonResponse({"message":"Operator did not found!.."})
        api_data = APIManager.objects.get(id=pdata.api_id.id)
        transection_number = uuid.uuid4()
        
        
        user = request.user
        user_profile = UserProfile.objects.get(user= user)
        
        if(user.wallet_ammount < float(amount)):
            return JsonResponse({"message":"Low balance, kindly recharge your wallet"})
        
        if(user_profile.transection_pin != pin):

            return JsonResponse({"message":"Transection pin is incorrect"})
        if(user_profile.status !="active"):
            return JsonResponse({"message":"Your account has been blocked"})
        
        if(pdata.status !=True):
            return JsonResponse({"message":"Operator Currently down!"})
        if(api_data.status !=True):
            return JsonResponse({"message":"Recharge Service Currently down!"})
        argumentss = {"transection_number":transection_number,"username": api_data.username,"token": api_data.password, "api_code":api_data.type, "api_url":api_data.url, "number":number, "amount":amount, "opcode":pdata.re_1 }
        scheme = Scheme.objects.get(id= 1)
        commission = Commission.objects.get(scheme_id=scheme.id,com_type_id=1, operator_id=pdata.id )
        if(commission.type == "percent"):
            profit = (float(amount)*float(commission.retailer))/100
        elif(commission.type == "fixed"):
            profit = commission.retailer
        else:
            profit=0
        report_data = Reports.objects.create(number =number,
                phone =user.phone,
                provider = pdata,
                api =api_data,
                amount = amount,
                profit = profit,
                txn_id  = transection_number,
                status = 'pending',
                credit_by =user,
                user_id= user,
                
                # 'credit_by => $user->id,
                r_type = 'main',
                via  = 'portal',
                balance = user.wallet_ammount,
                transection_type = 'debit',
                product    = 'recharge')
    # RechargeServiceType(argumentsss)
    match argumentss["api_code"]:
        case "recharge1":
            
            api_url = "{}recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["api_url"],argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], argumentss["transection_number"] )
            response = requests.get(f"{api_url}")
            print(api_url)
            if(response.status_code == 200):
                print(response.json())
                api_reponse = response.json()
                # break
                # return response
            else:
                return 400
            # return api_url
        case "recharge2":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge3":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge4":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case default:
            return "something went wrong"
    match argumentss["api_code"]:
        case "recharge1":
            if(api_reponse["status"] == "Success"):
                
                report_data.status = "Success"
                report_data.pay_id = api_reponse["txid"]
                report_data.api_txn_id = api_reponse["txid"]
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["opid"]
                
            elif(api_reponse["status"] == "Failure"):
                print("failed")
                report_data.status = "Failed"
                report_data.pay_id = ""
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["opid"]

            else:
                report_data.status = "Failed"
                report_data.pay_id = ""
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["opid"]
            # return api_url
        case "recharge2":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge3":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge4":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case default:
            return "something went wrong"
    if(report_data.status == "Success"):
        
        report_data.tds = (float(profit)*5)/100
        report_data.r_profit = float(profit) - ((float(profit)*5)/100)
        user.wallet_ammount = (float(user.wallet_ammount) - float(amount)) +float(report_data.r_profit)
        user.save()
        report_data.save()
        return JsonResponse({"message":"Recharge done successfully"})
    else:
        report_data.save()
        return JsonResponse({"message" : "something went wrong!..."})
        
    
     
    # return JsonResponse({"message":"request submitted successfully"})


        
def DTH_Recharge(request):
    rdata = Provider.objects.filter(type="dth")
    return render(request, "dth-recharge.html", {"rdata":rdata})
@login_required(login_url='login')
def DTHRechargeRequest(request):
    if(request.method == "POST"):
        # import pdb; pdb.set_trace()
        operator = request.POST.get("operator")
        number = request.POST.get("number")
        amount = request.POST.get("amount")
        pin = request.POST.get("pin")
        # user = request.POST.get("pin")
        try:
            pdata = Provider.objects.get(name=operator)
        except:
            return JsonResponse({"message":"Operator did not found!.."})

        api_data = APIManager.objects.get(id=pdata.api_id.id)
        transection_number = uuid.uuid4()
        user = request.user
        user_profile = UserProfile.objects.get(user= user)
        if(user.wallet_ammount < float(amount)):
            return JsonResponse({"message":"Low balance, kindly recharge your wallet"})
        
        import pdb; pdb.set_trace()
        if(user_profile.transection_pin != pin):

            return JsonResponse({"message":"Transection pin is incorrect"})
        if(user_profile.status !="active"):
            return JsonResponse({"message":"Your account has been blocked"})
        
        if(pdata.status !=True):
            return JsonResponse({"message":"Operator Currently down!"})
        if(api_data.status !=True):
            return JsonResponse({"message":"Recharge Service Currently down!"})
        argumentss = {"transection_number":transection_number,"username": api_data.username,"token": api_data.password, "api_code":api_data.type, "api_url":api_data.url, "number":number, "amount":amount, "opcode":pdata.re_1 }
        report_data = Reports.objects.create(number =number,
                phone =user.phone,
                provider = pdata,
                api =api_data,
                amount = amount,
                profit = "0.5",
                txn_id  = transection_number,
                status = 'pending',
                credit_by =user,
                user_id= user,
                
                # 'credit_by => $user->id,
                r_type = 'main',
                via  = 'portal',
                balance = user.wallet_ammount,
                transection_type = 'debit',
                product    = 'dth')
    # RechargeServiceType(argumentsss)
    match argumentss["api_code"]:
        case "recharge1":
            
            api_url = "{}recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["api_url"],argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], argumentss["transection_number"] )
            response = requests.get(f"{api_url}")
            print(api_url)
            if(response.status_code == 200):
                print(response.json())
                api_reponse = response.json()
                # break
                # return response
            else:
                return 400
            # return api_url
        case "recharge2":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge3":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge4":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case default:
            return "something went wrong"
    match argumentss["api_code"]:
        case "recharge1":
            if(api_reponse["status"] == "Success"):
                
                report_data.status = "Success"
                report_data.pay_id = api_reponse["txid"]
                report_data.api_txn_id = api_reponse["txid"]
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["message"]
            elif(api_reponse["status"] == "Failure"):
                print("failed")
                report_data.status = "Failed"
                report_data.pay_id = ""
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["message"]

            else:
                report_data.status = "Failed"
                report_data.pay_id = ""
                report_data.ref_id = api_reponse["opid"]
                report_data.description = api_reponse["message"]
            # return api_url
        case "recharge2":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge3":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case "recharge4":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argumentss["username"],argumentss["token"], argumentss["opcode"], argumentss["number"], argumentss["amount"], transection_number )
            return api_url
        case default:
            return "something went wrong"

    if(report_data.status == "Success"):
        report_data.save()
        return JsonResponse({"message":"request submitted successfully"})
    else:
        report_data.save()
        return JsonResponse({"message" : "something went wrong!..."})
    
def profileUpdate(request):
     if request.method == "POST":
        action = request.POST.get("action")
        if action == "profile_update":
            id = request.POST.get("id")
            name = request.POST.get("name")
            state = request.POST.get("state")
            city = request.POST.get("city")
            pin_code = request.POST.get("pin_code")
            address = request.POST.get("address")
            user = Account.objects.get(id = int(id))
            user.name = name
            user.save()
            user_profile = UserProfile.objects.get(user = user)
            user_profile.state = state
            user_profile.city = city
            user_profile.pin_code = pin_code
            user_profile.address = address
            user_profile.save()
            return JsonResponse({"message":"Profile Updated Sucessfully!"})
        
        if action == "kyc_update":
            id = request.POST.get("id")
            shop_name = request.POST.get("shop_name")
            gstin = request.POST.get("gstin")
            pan_card = request.POST.get("pan_card")
            aadhar_card = request.POST.get("aadhar_card")
            user = Account.objects.get(id = int(id))
            user_profile = UserProfile.objects.get(user = user)
            user_profile.shop_name = shop_name
            user_profile.gstin = gstin
            user_profile.pan_card = pan_card
            user_profile.aadhar_card = aadhar_card
            user_profile.save()
            return JsonResponse({"message":"KYC Updated Sucessfully!"})
        
        if action == "bank_update":
            id = request.POST.get("id")
            bank_ifsc = request.POST.get("bank_ifsc")
            holder_name = request.POST.get("holder_naame")
            bank_name = request.POST.get("bank_name")
            account_number = request.POST.get("account_number")
            user = Account.objects.get(id = int(id))
            user_profile = UserProfile.objects.get(user = user)
            user_profile.bank_ifsc = bank_ifsc
            user_profile.bank_name = bank_name
            user_profile.account_number = account_number
            user_profile.bank_holder_name = holder_name
            user_profile.save()
            return JsonResponse({"message":"Bank Updated Sucessfully!"})
        return JsonResponse({"message":"request submitted successfully"})
   

@login_required(login_url='login')
def ReportsDTHModule(request):
    recharge_data = []
    user = request.user
    reports_data = Reports.objects.filter(user_id = user, product="dth")
    for state in reports_data:
        # print(state)
        rep_data = {
        "status":state.status, "amount":state.amount, "txn_id":state.txn_id, "number":state.number
        }
        # print(rep_data)
        recharge_data.append(rep_data)
    return JsonResponse({"data":recharge_data})

def FastTagRecharge(request):
    return render(request, "fasttag-recharge.html")



## change transection pin

def ChangeTransectionPin(request):
    if(request.method == "POST"):
        new_pin = request.POST.get("otp_pin")
        otp = request.POST.get("otp")
        user = request.user
        user_profile = UserProfile.objects.get(user= user.id)
        if(user_profile.otp != otp):
            return JsonResponse({"message":"otp did not matched", "mtype":"failed"})
        user_profile.transection_pin = new_pin
        user_profile.save()
        return JsonResponse({"message":"Transection pin changed successfully", "mtype":"success"})

## GET OTP AAdhar

def getOTPAadhar(request):
    api_data = APIManager.objects.get(type="verification")
    if(request.method == "POST"):
        aadhar = request.POST.get("aadhar")
        api_url = "{}verification/get_aadhaar_otp?username={}&token={}&aadhaar_no={}".format(api_data.url, api_data.username, api_data.password, aadhar )
        print(api_url)
        response = requests.get(f"{api_url}")
        rsp_data = response.json()
        print(rsp_data)
        if(rsp_data["status"] == "Success"):
            rdata = {"refid":rsp_data["ref_id"], "message":rsp_data["message"], "status":rsp_data["status"]}
        else:
            rdata = {"status":"Failure", "message":"Something went wrong"}
    return JsonResponse({"data":rdata })

def VerifyAadhar(request):
    api_data = APIManager.objects.get(type="verification")
    user = request.user
    user_profile = UserProfile.objects.get(user = user.id)
    if(request.method == "POST"):
        aadhar = request.POST.get("aadhar")
        ref_id = request.POST.get("ref_id")
        otp = request.POST.get("otp")
        orderid = uuid.uuid4()
        api_url = "{}verification/api?username={}&token={}&opcode=AKYC&number={}&ref_id={}&otp={}&orderid={}&format=json".format(api_data.url, api_data.username, api_data.password, aadhar, ref_id,otp, orderid  )
        print(api_url)
        response = requests.get(f"{api_url}")
        rsp_data = response.json()
        print(rsp_data)
        if(rsp_data["status"] == "Success"):
            if(rsp_data["registered_name"] == user.name):
                user_profile.aadhar_card = aadhar
                user_profile.address = rsp_data["address"]
                user_profile.pin_code = rsp_data["pincode"]
                user_profile.state = rsp_data["state"]
                user_profile.city = rsp_data["dist"]
                user_profile.is_account = True
                user_profile.is_aadhar = True
                if(user_profile.is_aadhar == True and user_profile.is_pan == True and user_profile.is_account == True):
                    user_profile.kyc == "Pending For Approval"
                user_profile.save()
                rdata = { "message":"Aadhar verification successfull", "status":rsp_data["status"],"name":rsp_data["registered_name"] }
            else:
                rdata = { "message":"Your name and aadhar name not matched, try again", "status":"NO" ,"name":rsp_data["registered_name"]   }
            
        else:
            rdata = {"status":"Failure", "message":rsp_data["message"]}
    return JsonResponse({"data":rdata })
        


def VerifyPancard(request):
    api_data = APIManager.objects.get(type="verification")
    user = request.user
    user_profile = UserProfile.objects.get(user = user.id)
    if(request.method == "POST"):
        pancard = request.POST.get("pancard")
        orderid = uuid.uuid4()
        api_url = "{}verification/pan_verification?username={}&token={}&number={}&orderid={}&format=json".format(api_data.url, api_data.username, api_data.password, pancard, orderid  )
        print(api_url)
        response = requests.get(f"{api_url}")
        rsp_data = response.json()
        print(rsp_data)
        if(rsp_data["status"] == "Success"):
            if(rsp_data["opid"].upper() == request.user.name.upper()):
                user_profile.pan_card = pancard
                user_profile.is_pan = True
                if(user_profile.is_aadhar == True and user_profile.is_pan == True and user_profile.is_account == True):
                    user_profile.kyc == "Pending For Approval"
                user_profile.save()
                rdata = { "message":"Pancard verification successfull", "status":rsp_data["status"], "name":rsp_data["opid"]}
            else:
                rdata = { "message":"Your name and pancard name not matched, try again", "status":"NO"  ,"name":rsp_data["opid"]  }
            
        else:
            rdata = {"status":"Failure", "message":rsp_data["message"]}
    return JsonResponse({"data":rdata })
        
def VerifyGStNumber(request):
    api_data = APIManager.objects.get(type="verification")
    user = request.user
    user_profile = UserProfile.objects.get(user = user.id)
    if(request.method == "POST"):
        gstnumber = request.POST.get("gstnumber")
        orderid = uuid.uuid4()
        api_url = "{}verification/gst_verification?username={}&token={}&number={}&orderid={}&format=json".format(api_data.url, api_data.username, api_data.password, gstnumber, orderid  )
        print(api_url)
        response = requests.get(f"{api_url}")
        rsp_data = response.json()
        print(rsp_data)
        if(rsp_data["status"] == "Success"):
            user_profile.gstin = gstnumber  
            user_profile.shop_name = rsp_data["opid"]["legal_name_of_business"]
            user_profile.save()
            rdata = { "message":"GST verification successfull", "status":rsp_data["status"], "shop_name":rsp_data["opid"]["legal_name_of_business"]}
            
        else:
            rdata = {"status":"Failure", "message":rsp_data["message"]}
    return JsonResponse({"data":rdata })
    

## get main otp function 
def GetOTPMain(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    # company = Company.objects.get(user_id=user.id)
    otp= random.randint(0000, 9999)
    user_profile.otp = otp
    user_profile.save()
    app_signature_id ="vhbj"
    url ='https://sms.digidonar.com/app/smsapi/index.php?key=36311EFC53F988&campaign=11473&routeid=101494&type=text&contacts={}&senderid=RRAKLE&msg=Hello, Please use OTP {} to login to your Rationcart Account and shop from our wide array of products app_signature_id RAKLE&template_id=1507166582684980232&pe_id=1501641540000051921'.format(user.phone, otp)
    # sms_text = f"Hello, Please use OTP {otp} to login to your Rationcart Account and shop from our wide array of products {app_signature_id} RAKLE"
    # api_url = f"{company.sms_url}?key={company.sms_user_id}&campaign=11473&routeid=101494&type=text&contacts={user.phone}&senderid={company.sender_id}&msg={sms_text}&template_id={company.sms_password}&pe_id={company.sms_uti}"
    # print(api_url)
    response = requests.post(url)
    print(response.content)
    if(response.status_code == 200):
        print(response)
        return JsonResponse({"message":"otp sent successfully on registered mobile"})
    else:
        return JsonResponse({"message":"something went wrong! please try again"})
    # except:
    #     return JsonResponse({"message":"something went wrong! please try again pnce"})

def LoadWalletAmount(request):
    message= ""
    mtype=""
    user = request.user
    cdata = UserProfile.objects.filter(user = user.id)
    
    if(request.method == "POST"):
        action = request.POST.get("action")
        if(action == "create_request"):
            dep_bank = request.POST.get("deposit_bank")
            amount = request.POST.get("amount")
            payment_mode = request.POST.get("payment_mode")
            pay_date = request.POST.get("pay_date")
            ref_num = request.POST.get("ref_num")
            pay_slip = request.FILES.get("pay_slip")
            remark = request.POST.get("remark")
            requested_by = user
            try:
                LoadWalletRequest.objects.create(bankname=dep_bank, amount=amount, payment_mode=payment_mode, pay_date=pay_date, ref_number= ref_num, remark=remark, slip=pay_slip, requested_by=requested_by)
                mtype = "success"
                message ="Request Submitted Successfully"
            except:
                mtype = "failed"
                message ="something went wrong!..."
        
    data = LoadWalletRequest.objects.filter(requested_by=user.id)

    return render(request, "load-wallet.html", {"data":cdata, "rdata":data, "mtype":mtype, "message":message})

def UpdateWalletRequest(request):
    if(request.method == "POST"):
        action = request.POST.get("action")
        if(action == "update_request"):
            id = request.POST.get("id")
            status = request.POST.get("status")
            remark = request.POST.get("remark")
            accepted_by = request.user
            ldata = LoadWalletRequest.objects.get(id=id)
            ldata.accepted_by = accepted_by
            ldata.status = status
            ldata.remark = remark
            try:
                ldata.save()
                import pdb; pdb.set_trace()
                if(status == "approve"):
                    new_user = Account.objects.get(id= ldata.requested_by.id)
                    new_user.wallet_ammount = ldata.amount
                    new_user.save()
                mtype = "success"
                message ="Request Updated Successfully"
            except:
                mtype = "failed"
                message ="something went wrong!..."
        return JsonResponse({"mtype":mtype, "message":message})

def AEPSGateway(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    print(pdata.aeps_onboarding)
    return render(request, "aeps-gateway.html", {"eko_onboarding":pdata.eko_onboarding, "paysprint_on":pdata.aeps_onboarding})


def TwoFactorAuthenticationAEPS(request):
    user = request.user
    pdata = UserProfile.objects.get(user= user.id)
    print(pdata.aeps_onboarding)
    return render(request, "aeps_authentication.html",{"eko_onboarding":pdata.eko_onboarding, "paysprint_on":pdata.aeps_onboarding})
    