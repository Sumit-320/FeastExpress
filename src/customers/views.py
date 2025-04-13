from django.shortcuts import render,get_object_or_404,render,redirect 
from django.contrib.auth.decorators import login_required
from register.forms import UserProfileForm, UserInfoForm
from register.models import Profile2
from orders.models import Order, OrderedFood
from django.contrib import messages
import simplejson as json
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

def customerMyOrders(request):
    orders = Order.objects.filter(user = request.user,is_ordered = True).order_by('-created_at')# to get orders of logged in user
    context = {                                                          # '-' for reversed sorting 
        'orders':orders,
    }
    return render(request,'customers/my_orders.html',context)


def orderDetails(request,order_number):
    try: # to bring order details to my order page
        order = Order.objects.get(order_number = order_number,is_ordered=True) # to get order details for my order page
        ordered_food = OrderedFood.objects.filter(order = order)
        subtotal = 0
        for i in ordered_food:
            subtotal += i.price*i.quantity
        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food, 
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request,'customers/order_detail.html',context)
    except:
        return redirect('customer')
