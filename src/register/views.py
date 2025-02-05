from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, Profile2
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            email= form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            # create_user --> under class Manager to manage user profile
            user = User.objects.create_user(f_name=f_name,l_name=l_name,password=password,username=username,contact=contact,email=email)
            user.type = User.Buyer
            user.save()
            messages.success(request,"User Registered Successfully!")
            return redirect('registerUser')
        else:
            print(form.errors) # reason for invalid form
    else:
        form = UserForm()
        
    context = {
        'form':form,
    }
    return render(request,'register/registerUser.html',context)

def registerVendor(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        form_vendor= VendorForm(request.POST,request.FILES)
        if form.is_valid() and form_vendor.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            email= form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            user = User.objects.create_user(f_name=f_name,l_name=l_name,password=password,username=username,contact=contact,email=email)
            user.type= User.Seller
            user.save()
            vendor=form_vendor.save(commit=False)# data is preserved inside the object
            vendor.user=user
            profile=Profile2.objects.get(user=user)
            vendor.profile=profile
            vendor.save()
            messages.success(request,'Your Vendor Account is Registered, Wait for Approval')
            return redirect('registerVendor')
        else:
            print("The Form submitted is Invalid!")
            print(form.errors)

    else:
        form = UserForm()
        form_vendor= VendorForm()


    context = {
        'form':form,
        'form_vendor':form_vendor,
    }
    return render(request,'register/registerVendor.html',context)
