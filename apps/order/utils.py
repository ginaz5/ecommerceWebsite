import datetime
import os
from  random import randint
from apps.cart.cart import Cart
from apps.order.models import Order, OrderItem

# for api use
def checkout(request, first_name, last_name, email, address, zipcode, place):
    order = Order(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, place=place)
    order.save()

    cart = Cart(request)

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity']) # order is refer to above
    
    return order.id