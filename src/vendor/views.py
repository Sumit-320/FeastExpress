from django.shortcuts import render, get_object_or_404, redirect
from register.forms import UserProfileForm
from .forms import VendorForm
from register.models import Profile2
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from register.views import validateSeller

# Create your views here.
@login_required(login_url='login')
@user_passes_test(validateSeller)
def vProfile(request):
    profile = get_object_or_404(Profile2,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method=='POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance = profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance = vendor) # request.FILES for License image Upload
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Updated Successfully!')
            return redirect('vProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor) # loads the content of vendor form

    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html',context)