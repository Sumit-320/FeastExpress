from django.shortcuts import render, get_object_or_404, redirect
from register.forms import UserProfileForm
from .forms import VendorForm, OpeningHourForm
from register.models import Profile2
from .models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from register.views import validateSeller
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from orders.models import Order, OrderedFood
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

@login_required(login_url='login')
@user_passes_test(validateSeller)
def addCategory(request):
    if request.method=='POST':
       form = CategoryForm(request.POST)
       if form.is_valid():
            category_name = form.cleaned_data['category_name'] # sent via user via request POST
            category = form.save(commit=False)
            category.vendor = Vendor.objects.get(user=request.user)
            
            category.save()  # in the database
            category.slug = slugify(category_name)+'-'+str(category.id) # category id from saved catgeory
            messages.success(request,'Category Added Successfully!')
            return redirect('menuBuilder')
       else:
           print(form.errors)
    else: 
        form = CategoryForm()

    context={
        'form':form,
    }

    return render(request,'vendor/add_category.html',context) #now this category form is available to html

@login_required(login_url='login')
@user_passes_test(validateSeller)
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
           print(form.errors)
    else: 
        form = CategoryForm(instance=category) # instance containes data of existing category in the form

    context={
        'category':category,
        'form':form,
    }

    return render(request,'vendor/edit_category.html',context)

@login_required(login_url='login')
@user_passes_test(validateSeller)
def deleteCategory(request,pk=None):
    category = get_object_or_404(Category,pk=pk) # users' instance via pk
    category.delete()
    messages.success(request,'Category Deleted Successfully!')
    return redirect('menuBuilder')

@login_required(login_url='login')
@user_passes_test(validateSeller)
def addFood(request):
    if request.method=='POST':
       form = FoodItemForm(request.POST,request.FILES) # for img file
       if form.is_valid():
            food_title = form.cleaned_data['food_title'] # sent via user via request POST
            food = form.save(commit=False)
            food.vendor = Vendor.objects.get(user=request.user)
            food.sulg = slugify(food_title)
            form.save()  # in the database
            messages.success(request,'Food Item Added Successfully!')
            return redirect('foodByCategories',food.category.id)  # pk passed too!
       else:
           print(form.errors)
    else: 
        form = FoodItemForm()
        # to filter the different values for different vendors in menu-builder and food categories
        form.fields['category'].queryset = Category.objects.filter(vendor = Vendor.objects.get(user=request.user))

    context={
        'form':form,
    }
    return render(request,'vendor/add_food.html',context)

@login_required(login_url='login')
@user_passes_test(validateSeller)
def editFood(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk) # users' pk

    if request.method=='POST':
       form = FoodItemForm(request.POST,request.FILES,instance=food)
       if form.is_valid():
            food_title = form.cleaned_data['food_title'] # sent via user via request POST
            food = form.save(commit=False)  # food-object
            food.vendor = Vendor.objects.get(user=request.user)
            food.sulg = slugify(food_title)
            form.save()  # in the database
            messages.success(request,'Food Item Updated Successfully!')
            return redirect('foodByCategories',food.category.id)
       else:
           print(form.errors)
    else: 
        form = FoodItemForm(instance=food) # instance containes data of existing category in the form
        # to filter the different values for different vendors in menu-builder and food categories
        form.fields['category'].queryset = Category.objects.filter(vendor = Vendor.objects.get(user=request.user))
    context={
        'food':food,
        'form':form,
    }

    return render(request,'vendor/edit_food.html',context)

@login_required(login_url='login')
@user_passes_test(validateSeller)
def deleteFood(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk) # users' instance via pk
    food.delete()
    messages.success(request,'Food Item is Deleted Successfully!')
    return redirect('foodByCategories',food.category.id)

def openingHours(request):
    opening_hours = OpeningHour.objects.filter(vendor = Vendor.objects.get(user = request.user ))
    form = OpeningHourForm()
    context={
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request,'vendor/opening_hours.html',context)

def addOpeningHours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest' and request.method =='POST':  # ajax request
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                hour = OpeningHour.objects.create(vendor = Vendor.objects.get(user = request.user),
                                                  day=day,
                                                  from_hour=from_hour,
                                                  to_hour=to_hour,
                                                  is_closed=is_closed) 
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':  'success','id':hour.id,'day':day.get_day_display(),'is_closed':'Closed'}
                    else:
                        response = {'status':  'success','id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour, 'to_hour':hour.to_hour}

                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':  'failed','message':from_hour+'-'+to_hour+'already exists for this day!','error':str(e)}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid Reqest')

def removeOpeningHours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':  # ajax request
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})

def orderDetail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order = order,fooditem__vendor = Vendor.objects.get(user = request.user))  # fooditem has a FK to orders model
        context={
            'order': order,
            'ordered_food':ordered_food,
        }
    except:
        return redirect('vendors')
    
    return render(request,'vendor/order_detail.html',context)