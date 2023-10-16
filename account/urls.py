from django.urls import path

from . import views
from . import ReportsViews
from . import DMTViews
urlpatterns = [
    path('', views.index, name="index"),
    path('super_distibuter', views.superDistibuter, name = "super_distibuter"),
    path('login', views.login, name = 'login'),
    path('register', views.registration, name = 'register'),
    path('logout', views.logout, name = 'logout'),
    path('scheme_manager', views.SchemeManager, name = 'scheme_manager'),
    path('role_manager', views.roleManager, name = 'role_manager'),
    path('company', views.company, name = 'company'),
    path('commission_type_manager', views.CommissionTypeManager, name = 'commission_type_manager'),
    path('api_manager', views.apiManager, name = 'api_manager'),
    path('provider_manager', views.ProviderManager, name = 'provider_manager'),
    path('delete_scheme', views.DeleteScheme, name = 'delete_scheme'),
    path('edit_scheme', views.editScheme, name = 'edit_scheme'),
    path('add_scheme', views.AddScheme, name = 'add_scheme'),
    path('delete_commission_type', views.DeleteCommssionType, name = 'delete_commission_type'),
    path('edit_commission_type', views.editCommissionType, name = 'edit_commission_type'),
    path('add_commission_type', views.AddCommissionType, name = 'add_commission_type'),
    path('whitelabel_client', views.whitelabel, name = 'whitelabel_client'),
    path('super_distributer', views.superDistributer, name = 'super_distributer'),
    path('distributer', views.Distributer, name = 'distributer'),
    path('retailer', views.Retailer, name = 'retailer'),
    path('add_commission', views.AddCommission, name = 'add_commission'),
    path('get_commission_by_scheme', views.GetCommissionBySchemeAndCType, name = 'get_commission_by_scheme'),
    path('get_provider_by_id', views.GetProviderDataBYID, name = 'get_provider_by_id'),
    path('profile_manager/<int:id>', views.ProfileManager, name = 'profile_manager'),
    path('change_password', views.ChangePassword, name = 'change_password'),
    path('mobile_recharge', views.MobileRecharge, name = 'mobile_recharge'),
    path('create_mobile_recharge', views.MobileRechargeRequest, name = 'create_mobile_recharge'),
    path('profile_wl_update', views.profileUpdate, name = 'profile_wl_update'),
    path('dth_recharge', views.DTH_Recharge, name = 'dth_recharge'),
    path('create_dth_recharge', views.DTHRechargeRequest, name = 'create_dth_recharge'),
    path('report_dth_recharge', views.ReportsDTHModule, name = 'report_dth_recharge'),
    path('get_otp', views.GetOTPMain, name = 'get_otp'),
    path('change_transection_pin', views.ChangeTransectionPin, name = 'change_transection_pin'),
    path('load_wallet_amount', views.LoadWalletAmount, name = 'load_wallet_amount'),
    path('update_wallet_request', views.UpdateWalletRequest, name = 'update_wallet_request'),
    path('fasttag_recharge', views.FastTagRecharge, name = 'fasttag_recharge'),
    path('user_profile', views.UserProfileManager, name = 'user_profile'),
    path('fetch_location', views.FetchCurrentLocation  , name = 'fetch_location'),
    path('get_otp_aadhar', views.getOTPAadhar  , name = 'get_otp_aadhar'),
    path('verify_aadhar', views.VerifyAadhar  , name = 'verify_aadhar'),
    path('verify_pancard', views.VerifyPancard  , name = 'verify_pancard'),
    path('verify_gstnumber', views.VerifyGStNumber  , name = 'verify_gstnumber'),

    ## report url
    path('recharge_report', ReportsViews.RechargeReport, name = 'recharge_report'),
    path('get_recharge_report', ReportsViews.GetRechargeReportsData, name = 'get_recharge_report'),
    path('show_receipt_recharge', ReportsViews.ShowReceiptRecharge, name = 'show_receipt_recharge'),
    path('aeps_authentication_all', views.TwoFactorAuthenticationAEPS, name = 'aeps_authentication_all'),


    ## DMT Views
    path('money_transfer', DMTViews.DMTRetailerOnBoard, name = 'money_transfer'),
    path('aeps', views.AEPSGateway, name = 'aeps'),
    path('aeps_payment', DMTViews.EKOAEPS, name = 'aeps_payment'),
 
    ## Paysprint AEPS Views 
    path('aeps_bank_list_1', DMTViews.PAEPSBankList, name = 'aeps_bank_list_1'),
    path('aeps_onboarding', DMTViews.PAEPS_Onboardiing, name = 'aeps_onboarding'),
    path('aeps_authentication', DMTViews.PAEPSDailyAuthentication, name = 'aeps_authentication'),


]
