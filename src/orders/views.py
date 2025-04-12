from django.shortcuts import render, redirect
from market.models import Cart
from market.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
import simplejson as json
from .utils import generate_order_number
from django.http import HttpResponse
# Create your views here.

def placeOrder(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect('market')
    
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
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items,
            }
            return render(request,'orders/place_order.html',context)

        else:
            print(form.errors)
    return render(request,'orders/place_order.html')

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
        return HttpResponse('saved Ordered food')
    return HttpResponse("payments views")