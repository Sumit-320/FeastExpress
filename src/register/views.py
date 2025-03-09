from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages, auth
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, Profile2
from .utils import detect, verify_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already registered!!")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            email= form.cleaned_data['email']
            # create_user --> under class Manager to manage user profile
            user = User.objects.create_user(f_name=f_name,l_name=l_name,username=username,password=password,email=email)
            user.type = User.Buyer
            user.save() 

            # email verification of customer
            verify_email(request,user)
            messages.success(request,"User Registered Successfully!")
            return redirect('signup')
        else:
            print(form.errors) # reason for invalid form
    else:
        form = UserForm()
        
    context = {
        'form':form,
    }
    return render(request,'register/registerUser.html',context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already registered!!")
        return redirect('redirectAccount')
    elif request.method=='POST':
        form = UserForm(request.POST)# to pass the contents from post request
        v_form  = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid:
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            email= form.cleaned_data['email']
            user = User.objects.create_user(f_name=f_name,l_name=l_name,username=username,password=password,email=email)
            user.type= User.Seller
            user.save()
            vendor=v_form.save(commit=False)# data is preserved inside the object
            vendor.user=user
            u_profile=Profile2.objects.get(user=user)
            vendor.profile=u_profile
            vendor.save()
            # verify the vendor
            verify_email(request,user)
            messages.success(request,'Your Vendor Account is Registered, Wait for Approval')
            return redirect('registerVendor')
        else:
            print("The Form submitted is Invalid!")
            print(form.errors)

    else:
        form = UserForm()
        v_form= VendorForm()


    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request,'register/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are Logged In!")
        return redirect('redirectAccount')
    if request.method=='POST':
        email = request.POST['email']#name of input field of sign-in form
        password= request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None: # -->user exists
            auth.login(request,user)
            messages.success(request,'Logged In Successfully!')
            return redirect('redirectAccount')
        else:
            messages.error(request,"Invalid Credentials, Please Try Again!")
            return redirect('login')

    return render(request,'register/login.html')

def signup(request):
    return render(request,'register/signup.html')

def validateSeller(user):
    if user.type==1:
        return True
    else:
        raise PermissionDenied # displays 403 forbidden-http error on webpage
    
def validateCustomer(user):
    if user.type==2:
        return True
    else:
        raise PermissionDenied
    

@login_required(login_url='login')# redirects user to /login if not logged in
def redirectAccount(request):
    user = request.user
    redirectUrl=detect(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(validateCustomer)# decorator used to restric users from accessing views 
def customerDashboard(request):
    return render(request,'register/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(validateSeller)
def vendorDashboard(request):
    return render(request,'register/vendorDashboard.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,"Logged Out Successfully!")
    return redirect('login')

def activate(request,uidb64,token):
    #user verification via otp-token
    return