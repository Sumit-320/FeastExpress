from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
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
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request,'register/registerUser.html',context)
