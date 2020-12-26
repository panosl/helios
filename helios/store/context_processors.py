# -*- coding: utf-8 -*-
import pickle
from importlib import import_module

from helios.conf import settings

Cart = getattr(import_module(settings.CART), 'Cart')


def cart(request):
    if not request.session.get('cart'):
        cart = Cart(user=request.user)
        request.session['cart'] = str(pickle.dumps(cart, protocol=0), 'latin-1')

    try:
        # failsafe for old request carts
        cart = pickle.loads(bytes(request.session['cart'], 'latin-1'))
    except UnicodeDecodeError:
        del request.session['cart']
        cart = Cart(user=request.user)
        request.session['cart'] = str(pickle.dumps(cart, protocol=0), 'latin-1')

    try:
        if Cart.version > cart.version:
            raise AttributeError
    except AttributeError:
        del request.session['cart']
        cart = Cart(user=request.user)
        # request.session['cart'] = pickle.dumps(cart)
        request.session['cart'] = str(pickle.dumps(cart, protocol=0), 'latin-1')
        # cart = pickle.loads(request.session['cart'])
        cart = pickle.loads(bytes(request.session['cart'], 'latin-1'))

    cart.update_with_user(request.user)

    # request.session['cart'] = pickle.dumps(cart)
    request.session['cart'] = str(pickle.dumps(cart, protocol=0), 'latin-1')

    return {'cart': pickle.loads(bytes(request.session['cart'], 'latin-1'))}
