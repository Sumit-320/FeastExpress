from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart

# Create your views here.
def market(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active = True)[:12]  # user model's is_active
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'market/listings.html',context)

def vendorDetail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug =vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(  # looks for data in reversed manner 
        Prefetch( # we dont have fooditem FK in model category  --> reverse lookup
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'market/vendor_detail.html',context)

def addToCart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    checkCart = Cart.objects.get(user = request.user,fooditem = fooditem) # only run if authenticated
                    # increase cart qty
                    checkCart.quantity +=1
                    checkCart.save()
                    return JsonResponse({'status':'Success','message':'Increased Successfully!'})
                except:
                    checkCart = Cart.objects.create(user = request.user,fooditem = fooditem,quantity=0) # only run if authenticated
                    # increase cart qty
                    checkCart.quantity +=1
                    checkCart.save()
                    return JsonResponse({'status':'Success','message':'Added Successfully!'})
            except:
                return JsonResponse({'status':'Failed','message':'Sorry, this item doesnt exist!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
    return JsonResponse({'status':'Failed','message':'Please Login to your account to continue'})