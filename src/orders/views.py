from django.shortcuts import render, redirect
from market.models import Cart
from market.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
import simplejson as json
from .utils import generate_order_number
from django.http import HttpResponse, JsonResponse
from register.utils import send_notification
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url= 'login')
def placeOrder(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect('market')
    vendor_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendor_ids:
            vendor_ids.append(i.fooditem.vendor.id)
    print(vendor_ids)
    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']

    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # order id is generated for order_number field
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendor_ids)  # recursively add
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items,
            }
            return render(request,'orders/place_order.html',context)

        else:
            print(form.errors)
    return render(request,'orders/place_order.html')

@login_required(login_url= 'login')
def payments(request):
    # gonna store the payment details from paypal/razorpay
    if request.headers.get('x-requested-with')=='XMLHttpRequest' and request.method=='POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        order = Order.objects.get(user = request.user,order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id=  transaction_id,
            payment_method = payment_method,
            status = status,
            amount = order.total
        )
        payment.save()

        # order model update
        order.payment = payment
        order.is_ordered = True
        order.save() 
        # return HttpResponse('Saved')  - to check 
        cart_items = Cart.objects.filter(user = request.user)
        # to save order after customers successful payment!
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity 
            ordered_food.save()
        #return HttpResponse('saved Ordered food')


        # conf mail to buyer
        mail_subject = 'Thank you for ordering ! - Team FeastExpress.'
        mail_template = 'orders/order_confirmation_email.html'

        ordered_food = OrderedFood.objects.filter(order=order)
        customer_subtotal = 0
        for item in ordered_food:
            customer_subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
             'ordered_food': ordered_food,
            'domain': get_current_site(request),
            'customer_subtotal': customer_subtotal,
            'tax_data': tax_data,
        }
        send_notification(mail_subject, mail_template, context)
        # return HttpResponse('email sent to user!')

        # mial to seller
        mail_subject = 'Hey! You have received a new order.'
        mail_template = 'orders/new_order_received.html'
        to_emails = []
        for i in cart_items:
            # bcz customer can order from multiple restaurants
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)  
                ordered_food_to_vendor = OrderedFood.objects.filter(order=order, fooditem__vendor=i.fooditem.vendor)
                #print(ordered_food_to_vendor)
                context = {
                    'order': order,
                    'to_email': i.fooditem.vendor.user.email,
                    'ordered_food_to_vendor': ordered_food_to_vendor,
                    # 'vendor_subtotal': order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'],
                    # 'tax_data': order_total_by_vendor(order, i.fooditem.vendor.id)['tax_dict'],
                    # 'vendor_grand_total': order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total'],
                }
                send_notification(mail_subject, mail_template, context)
        response = {
            'order_number':order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)
                
    return HttpResponse("payments views")

def orderComplete(request):
    # mentioned in the url upon payment
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number = order_number,payment__transaction_id = transaction_id,is_ordered = True)
        ordered_food = OrderedFood.objects.filter(order = order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price*item.quantity)

        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }

        return render(request,'orders/order_complete.html',context)
    except:
        return redirect('home')
    