from django.db import models
from django.contrib.auth.models import AbstractUser
from lib.models import BaseModel

# Create your models here.
class Role(BaseModel):
    name = models.CharField(max_length=250)



class Scheme(BaseModel):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    
class Account(AbstractUser):
    """
        Inherits from default User of Django and extends the fields.
        The following fields are part of Django User Model:
        | id
        | password
        | last_login
        | is_superuser
        | username
        | first_name
        | last_name
        | email
        | is_staff
        | is_active
        | date_joined
        """
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    wallet_ammount = models.FloatField(default=0.0)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]


class Company(BaseModel):
    company_name = models.CharField(max_length=250)
    sort_name = models.CharField(max_length=20)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company/')
    status = models.BooleanField()
    sender_id = models.CharField(max_length=200)
    sms_user_id = models.CharField(max_length=200)
    sms_password = models.CharField(max_length=200)
    sms_url = models.CharField(max_length=200)
    user = models.OneToOneField(Account, on_delete=models.CASCADE, unique=True)
    sms_uti = models.CharField(max_length=200)
    smtp_url = models.CharField(max_length=200)
    smtp_user_name = models.CharField(max_length=200)
    smtp_password = models.CharField(max_length=200)
    smtp_port = models.CharField(max_length=200)


class UserProfile(models.Model):
    otp = models.CharField(max_length=50, blank=True, null=True)
    otp_resend = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    shop_name = models.CharField(max_length=250, blank=True, null=True)
    gstin = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=7, blank=True, null=True)
    pan_card = models.CharField(max_length=50, blank=True, null=True)
    aadhar_card = models.CharField(max_length=50, blank=True, null=True)
    aadhar_card_front = models.ImageField(upload_to ='member/', blank=True, null=True)
    aadhar_card_back = models.ImageField(upload_to ='member/', blank=True, null=True)
    pan_card_pic = models.ImageField(upload_to='member/', blank=True, null=True)
    gstin_pic = models.ImageField(upload_to='member/', blank=True, null=True)
    profile_pic = models.ImageField(upload_to='member/', blank=True, null=True)
    kyc = models.CharField(max_length=50,default="pending", blank=True, null=True)
    callback_url = models.CharField(max_length=250, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    reset_password = models.BooleanField(default=False)
    bank_holder_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=50, blank=True, null=True)
    app_token = models.CharField(max_length=2000, blank=True, null=True)
    old_password = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)
    user = models.OneToOneField(Account,related_name="user", on_delete=models.CASCADE, null=True, blank=True)
    distributer = models.OneToOneField(Account,related_name="distributer", on_delete=models.CASCADE, null=True, blank=True)
    super_distributer = models.OneToOneField(Account,related_name="super_distributer", on_delete=models.CASCADE, null=True, blank=True)
    white_label = models.OneToOneField(Account,related_name="white_label", on_delete=models.CASCADE, null=True, blank=True)
    scheme = models.ForeignKey(Scheme, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    transection_pin = models.CharField(max_length=4,blank=True, null=True)
    eko_onboarding = models.BooleanField(default=False, blank=True, null=True)
    dob = models.CharField(max_length=250, default="1990-10-12", blank=True, null=True)
    aeps_onboarding =models.BooleanField(default=False, blank=True, null=True)
    is_gst =models.BooleanField(default=False, blank=True, null=True)
    is_pan =models.BooleanField(default=False, blank=True, null=True)
    is_aadhar =models.BooleanField(default=False, blank=True, null=True)
    is_account =models.BooleanField(default=False, blank=True, null=True)

class CommissionType(BaseModel):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

class APIManager(BaseModel):
    product_name = models.CharField(max_length=250)
    sort_name = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    status = models.BooleanField()
    api_key = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    optional = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
class Provider(BaseModel):
    name = models.CharField(max_length=250)
    re_1 = models.CharField(max_length=20)
    re_2 = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    re_3 = models.CharField(max_length=200)
    re_4 = models.CharField(max_length=200)
    api_id = models.ForeignKey(APIManager, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    logo = models.URLField(blank=True, null=True)
    com_type = models.ForeignKey(CommissionType, on_delete=models.CASCADE)
    is_mandatory = models.BooleanField(default=False)

class Circle(BaseModel):
    state_head = models.CharField(max_length=250)
    plan_code = models.CharField(max_length=20)
    state_code = models.CharField(max_length=200)
    


class Commission(BaseModel):
    com_type_id = models.ForeignKey(CommissionType, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    scheme_id = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    operator_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    white_label = models.CharField(max_length=200)
    super_distributor = models.CharField(max_length=200)
    distributor = models.CharField(max_length=200)
    retailer = models.CharField(max_length=200)

class Reports(BaseModel):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    api = models.ForeignKey(APIManager, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    credit_by = models.ForeignKey(Account,related_name="credit_by", on_delete=models.CASCADE)
    user_id = models.ForeignKey(Account,related_name="user_id",  on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    charge = models.CharField(max_length=200,  blank=True, null=True, )
    profit = models.CharField(max_length=200,  blank=True, null=True, )
    gst = models.CharField(max_length=200,  blank=True, null=True, )
    tds = models.CharField(max_length=200,  blank=True, null=True, )
    api_txn_id   = models.CharField(max_length=200, blank=True, null=True, )
    txn_id = models.CharField(max_length=200,  blank=True, null=True, )
    pay_id = models.CharField(max_length=200, blank=True, null=True, )
    ref_id = models.CharField(max_length=200, blank=True, null=True, )
    description = models.CharField(max_length=200, blank=True, null=True, )
    remark = models.CharField(max_length=200, blank=True, null=True, )
    optional_1 = models.CharField(max_length=200, blank=True, null=True, )
    optional_2 = models.CharField(max_length=200, blank=True, null=True, )
    optional_3 = models.CharField(max_length=200, blank=True, null=True, )
    optional_4 = models.CharField(max_length=200, blank=True, null=True, )
    status = models.CharField(max_length=200)
    r_type = models.CharField(max_length=200, blank=True, null=True, )
    via = models.CharField(max_length=200, blank=True, null=True, )
    balance = models.CharField(max_length=200, blank=True, null=True, )
    transection_type = models.CharField(max_length=200, blank=True, null=True, )
    product = models.CharField(max_length=200, blank=True, null=True, )
    w_profit = models.CharField(max_length=200, blank=True, null=True, )
    s_profit = models.CharField(max_length=200, blank=True, null=True, )
    d_profit = models.CharField(max_length=200, blank=True, null=True, )
    r_profit = models.CharField(max_length=200, blank=True, null=True, )

class LoadWalletRequest(BaseModel):
    bankname = models.CharField(max_length=500)
    amount = models.CharField(max_length=50)
    payment_mode = models.CharField(max_length=500)
    pay_date = models.CharField(max_length=500)
    ref_number = models.CharField(max_length=200)
    remark = models.CharField(max_length=500)
    slip = models.ImageField(upload_to='slip/')      
    requested_by = models.ForeignKey(Account,related_name="requested_by", on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(Account,related_name="accepted_by",  on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(default="pending", max_length=50)

class EkoBankList(BaseModel):
    BANK_NAME = models.CharField(max_length=50)
    SHORT_CODE = models.CharField(max_length=50)
    IMPS_STATUS = models.CharField(max_length=50)
    NEFT_STATUS = models.CharField(max_length=50)
    ISVERIFICATIONAVAILABLE = models.CharField(max_length=50)

    






