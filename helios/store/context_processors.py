# -*- coding: utf-8 -*-
import pickle
from importlib import import_module

from helios.conf import settings

Cart = getattr(import_module(settings.CART), 'Cart')


def cart(request):
    # del request.session['cart']
    if not request.session.get('cart'):
        cart = Cart(user=request.user)
        request.session['cart'] = pickle.dumps(cart)

    cart = pickle.loads(request.session['cart'])
    cart.update_with_user(request.user)
    request.session['cart'] = pickle.dumps(cart)

    return {'cart': pickle.loads(request.session['cart'])}
