from django.shortcuts import render, get_object_or_404, redirect
from register.forms import UserProfileForm
from .forms import VendorForm
from register.models import Profile2
from .models import Vendor
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from register.views import validateSeller
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
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

@login_required(login_url='login')
@user_passes_test(validateSeller)
def menuBuilder(request):
    vendor = Vendor.objects.get(user = request.user) # to get logged-in vendor
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(validateSeller)
def foodByCategories(request,pk=None):
    vendor=Vendor.objects.get(user=request.user)
    category =  get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    #print(fooditems)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/food_items_by_category.html',context)

def addCategory(request):
    if request.method=='POST':
       form = CategoryForm(request.POST)
       if form.is_valid():
            category_name = form.cleaned_data['category_name'] # sent via user via request POST
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.sulg = slugify(category_name)
            form.save()  # in the database
            messages.success(request,'Category Added Successfully!')
            return redirect('menuBuilder')
    else: 
        form = CategoryForm()

    context={
        'form':form,
    }

    return render(request,'vendor/add_category.html',context) #now this category form is available to html

def editCategory(request,pk=None):
    category = get_object_or_404(Category,pk=pk) # users' pk

    if request.method=='POST':
       form = CategoryForm(request.POST,instance=category)
       if form.is_valid():
            category_name = form.cleaned_data['category_name'] # sent via user via request POST
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            category.sulg = slugify(category_name)
            form.save()  # in the database
            messages.success(request,'Category Updated Successfully!')
            return redirect('menuBuilder')
    else: 
        form = CategoryForm(instance=category) # instance containes data of existing category in the form

    context={
        'category':category,
        'form':form,
    }

    return render(request,'vendor/edit_category.html',context)

def deleteCategory(request,pk=None):
    category = get_object_or_404(Category,pk=pk) # users' instance via pk
    category.delete()
    messages.success(request,'Category Deleted Successfully!')
    return redirect('menuBuilder')