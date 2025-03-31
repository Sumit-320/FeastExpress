from vendor.models import Vendor
from django.conf import settings

def getVendor(request): # to render same images/details of vendor mutliple times  (sidebar pages) in various HTML
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None   # for non-logged in users
    return dict(vendor=vendor)

def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}