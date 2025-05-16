from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages, auth
from .forms import UserForm
from datetime import datetime
from vendor.forms import VendorForm
from .models import User, Profile2
from orders.models import Order
from .utils import detect, send_email, reset_link
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
import datetime

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

            # email verification of customer using utility function
            mail_subject='FeastExpress Account Activation Mail'
            email_template='email/acc_verify.html'
            send_email(request,user,mail_subject,email_template)
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
            v_name = v_form.cleaned_data['name']
            vendor.vendor_slug = slugify(v_name)+'-'+str(user.id) # for concat always use str only
            u_profile=Profile2.objects.get(user=user)
            vendor.profile=u_profile
            vendor.save()
            # verify the vendor using utility function
            mail_subject='FeastExpress Account Activation Mail'
            mail_template='email/acc_verify.html'
            send_email(request,user,mail_subject,mail_template)
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
    elif request.method=='POST':
        email = request.POST.get('email')  # Avoid KeyError
        password = request.POST.get('password')

        user = auth.authenticate(email=email,password=password)
        if user is not None: # -->user exists
            auth.login(request,user)
            messages.success(request,'Logged In Successfully!')
            return redirect('redirectAccount')
        else:
            messages.error(request,"Invalid Credentials, Please Try Again!")
            return redirect('login')

    return render(request,'register/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"Logged Out Successfully!")
    return redirect('login')

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
    
def activate(request,uidb64,token):
    #user verification via otp-token
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # decode the encoded uid on verification email
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token): 
        user.is_active = True   # if verified-> set user active, so that he can log in
        user.save()
        messages.success(request, 'Account activated sucessfully!')
        return redirect('redirectAccount') # redirect to respective dashboard
    else:
        messages.error(request, 'Invalid link, Please try again!')
        return redirect('redirectAccount')


def forgotPassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email) #exact case-sensitive match with the provided email

            #send reset link using utility function
            mail_subject='Reset your password'
            mail_template='email/resetPassword.html'
            reset_link(request,user,mail_subject,mail_template)
            messages.success(request,'Password reset link sent successfully!')
            return redirect('login')
        else:
            messages.error(request,'This Email address is not registered!')
            return redirect('forgotPassword')
    return render(request,'register/forgotPassword.html')

def resetValidate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):# verify the token
        request.session['uid'] = uid # save uid(primary key) in session to use in resetting the password
        messages.info(request, "Reset your account's password")
        return redirect('resetAccountPassword')
    else:
        messages.error(request, 'This link is expired! Redirecting to you dashboard...')
        return redirect('redirectAccount')
    

def resetAccountPassword(request):
    if request.method=='POST':
        password= request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password: # refer line 170 --> we use the session id to reset password
            pk = request.session.get('uid') # pk of user seeking password reset!
            user = User.objects.get(pk=pk) # finding user data
            user.set_password(password) # reset password
            user.is_active=True 
            user.save()

            messages.success(request,'Password changed successfully!')
            return redirect('login')
        else:
            messages.error(request,'Passwords do not match!')

    return render(request,'register/resetAccountPassword.html')

@login_required(login_url='login')# redirects user to /login if not logged in
def redirectAccount(request):
    user = request.user
    redirectUrl=detect(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(validateCustomer)# decorator used to restric users from accessing views 
def customerDashboard(request):
    orders = Order.objects.filter(user = request.user,is_ordered = True)# to get orders of logged in user
    recent_orders= orders[:8]
    context = {
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
    }
    return render(request,'register/customerDashboard.html',context)

@login_required(login_url='login')
@user_passes_test(validateSeller)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)# req.user-> logged in user!
    orders = Order.objects.filter(vendors__in= [vendor.id],is_ordered=True).order_by('-created_at')
    recent_orders = orders[:7]

    current_month = datetime.datetime.now().month
    current_months_orders= orders.filter(vendors__in = [vendor.id], created_at__month = current_month)

    current_month_revenue = 0

    for i in current_months_orders:
        current_month_revenue+=i.get_total_by_vendor()['grand_total']

    total_revenue = 0
    for i in orders:
        total_revenue+=i.get_total_by_vendor()['grand_total']
    context={
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
        'total_revenue':total_revenue,
        'current_month_revenue':current_month_revenue,

    }
    return render(request,'register/vendorDashboard.html',context) # dynamically update vendor info in html
