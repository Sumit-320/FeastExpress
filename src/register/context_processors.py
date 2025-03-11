from vendor.models import Vendor


def getVendor(request): # to render same images/details of vendor mutliple times  (sidebar pages) in various HTML
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None   # for non-logged in users
    return dict(vendor=vendor)