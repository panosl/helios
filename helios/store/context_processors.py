# -*- coding: utf-8 -*-
import pickle
from helios.store.cart import Cart


def cart(request):
	if not request.session.get('cart'):
		cart = Cart()
		request.session['cart'] = pickle.dumps(cart)

	return {'cart': pickle.loads(request.session['cart'])}
