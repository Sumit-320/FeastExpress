from django.shortcuts import HttpResponse,render
from vendor.models import Vendor

def home(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active = True)[:12]  # user model's is_active
    context={
        'vendors':vendors,
    }
    return render(request,'home.html',context)