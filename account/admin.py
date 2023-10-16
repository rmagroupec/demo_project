from django.contrib import admin
from account.models import *
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'modified_at']

# admin.site.register(Role)
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name','sort_name','website','logo','status','sender_id','sms_user_id','sms_password','sms_uti','smtp_url','smtp_user_name','smtp_password','smtp_port']

@admin.register(Scheme)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','type','status']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','email','password','wallet_ammount','phone','role','created_at','modified_at','username']

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['otp','otp_resend','address','status','shop_name','gstin','gender','city','state','pin_code','pan_card','aadhar_card','aadhar_card_front','aadhar_card_back','pan_card_pic','gstin_pic','profile_pic','kyc','callback_url','remark','bank_holder_name','account_number','bank_name','bank_ifsc','app_token','created_at','modified_at','user','scheme','company']
