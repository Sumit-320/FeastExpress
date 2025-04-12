from vendor.models import Vendor
from django.conf import settings
from register.models import Profile2

def getVendor(request): # to render same images/details of vendor mutliple times  (sidebar pages) in various HTML
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None   # for non-logged in users
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = Profile2.objects.get(user = request.user)
    except:
        user_profile=None
    return dict(user_profile=user_profile)

def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID':settings.PAYPAL_CLIENT_ID}