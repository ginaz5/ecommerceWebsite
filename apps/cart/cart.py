from django.conf import settings

from apps.store.models import Product

class Cart(object):
    # initialization
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
    
    # get products from db
    def __iter__(self):

        for p, item in self.cart.items():
            item['product'] = Product.objects.get(pk=p)
            item['total_price'] = float(item['price']) * int(item['quantity']) # dollar might be float

            yield item

    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': price, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] +=1
        
        self.save()
    
    def remove(self, product_id):
        # check key exist in cart
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def get_total_cost(self):
        return sum(float(item['total_price']) for item in self) 