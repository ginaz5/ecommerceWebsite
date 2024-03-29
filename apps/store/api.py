import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from stripe.api_resources import line_item, payment_method

from apps.cart.cart import Cart
from .models import Product
from apps.order.utils import checkout # to get order id
from apps.order.models import Order
import stripe # to use token
from django.conf import settings

def create_checkout_session(request):
    cart = Cart(request)
    
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    items = []
    
    for item in cart:
        product = item['product']
        obj = {
            'price_data':{
                'currency':'usd',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': int(product.price * 100)
            },
            'quantity': item['quantity']
        }

        items.append(obj)

    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode = 'payment', 
        success_url = 'http://127.0.0.1:8000/cart/success',
        cancel_url = 'http://127.0.0.1:8000/cart/'
    )

    # Create order
    data = json.loads(request.body)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    payment_intent = session.payment_intent

    orderid = checkout(request, first_name, last_name, email, address, zipcode, place)

    # total_price = 0.00
    # for item in cart:
    #     total_price += (float(product.price)* int(item['quantity']))

    order = Order.objects.get(pk=orderid)
    order.payment_intent = payment_intent # check data from stripe
    order.paid_amount = cart.get_total_cost()
    order.paid = True
    order.save() 

    
    return JsonResponse({'session':session})


def api_checkout(request):
    cart = Cart(request)
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']

    orderid = checkout(request, first_name, last_name, email, address, zipcode, place)

    paid = True

    if paid == True:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()
        
        cart.clear()
    
    return JsonResponse(jsonresponse)

def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    
    # instance of cart, the request is initialization of the cart
    cart = Cart(request)

    # get product from database
    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)

    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id']) # fix string error in cart.remove

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)
