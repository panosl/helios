# -*- coding: utf-8 -*-
import pickle
from contextlib import contextmanager
from importlib import import_module

from django.contrib.auth.models import AnonymousUser

from helios.conf import settings


module_name, model_name = settings.PRODUCT_MODEL.rsplit('.', 1)
ProductModel = getattr(import_module(module_name), model_name)


class Cart(dict):
    """
    A dict-like object, which stores ``Product.id``:``CartLine`` pairs, in the form of:
    {ID: {'id': ID, 'quantity': QUANTITY}}

    Examples:

    >>> cart = Cart()
    >>> cart.add_product(id=1, quantity=20)
    """

    def __init__(self, user=AnonymousUser, **products):
    # def __init__(self, **products):
        super(Cart, self).__init__(products)
        self.user = user

    def add_product(self, product_id, quantity=1):
        """
        Add product to ``Cart``.

        If product already in ``Cart`` add to the quantity.
        """
        #if self.has_key(product_id):
        if product_id in self:
            self[product_id]['quantity'] += quantity
        else:
            self[product_id] = CartLine(user=self.user, id=product_id, quantity=quantity)

    def remove_product(self, product_id):
        del self[product_id]

    def get_product_list(self):
        """
        Return the product_list based on the currently stored IDs.
        """
        product_list = ProductModel.objects.in_bulk(self.keys())
        return product_list.values()

    def _get_product_count(self):
        return sum((product['quantity'] for product in self.itervalues()))

    def _get_price(self):
        """
        Sum and return the price of each ``CartLine``.
        """
        return sum((cart_line.price for cart_line in self.itervalues()))

    def dump(self):
        return pickle.dumps(self)

    def update_with_user(self, user):
        """
        Apply user to the cart and its ``CartLine``s.
        Once the cartlines have been added and a user logs in
        the user remains as AnonymousUser so we need to force it.
        """
        self.user = user

        for cl in self.itervalues():
            cl.user = self.user

    total_price = property(_get_price)
    product_count = property(_get_product_count)


class CartLine(dict):
    """
    """
    # def __init__(self, request=None, **line):
    def __init__(self, user=AnonymousUser, **line):
        super(CartLine, self).__init__(line)
        self.user = user

    def _get_product(self):
        product = ProductModel.objects.get(id__exact=self['id'])
        return product

    def get_quantity(self):
        return self['quantity']

    def set_quantity(self, quantity):
        self['quantity'] = quantity

    def _get_price(self):
        return self._get_product().price * self['quantity']

    product = property(_get_product)
    price = property(_get_price)


@contextmanager
def cart(request):
    # del request.session['cart']
    if not request.session.get('cart'):
        cart = Cart(user=request.user)
        request.session['cart'] = pickle.dumps(cart)
    session_cart = pickle.loads(request.session.get('cart'))
    session_cart.update_with_user(request.user)
    yield session_cart
    request.session['cart'] = session_cart.dump()
