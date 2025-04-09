from django.shortcuts import render,get_object_or_404,render,redirect 
from django.contrib.auth.decorators import login_required
from register.forms import UserProfileForm, UserInfoForm
from register.models import Profile2
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
def cProfile(request):
    profile = get_object_or_404(Profile2,user  = request.user)
    if request.method=='POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance = profile) # to auto - populate form based on db data
        user_form = UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated Successfully!')
            return redirect('cProfile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile) # to auto - populate form based on db data
        user_form = UserInfoForm(instance=request.user)
    

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render (request,'customers/cprofile.html',context)