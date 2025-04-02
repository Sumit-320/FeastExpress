from django.shortcuts import render
from vendor.models import Vendor

# Create your views here.
def market(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active = True)[:12]  # user model's is_active
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'market/listings.html',context)