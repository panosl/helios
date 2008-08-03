# -*- coding: utf-8 -*-
import pickle
#from store.views import Cart


def cart_required(view_func):
	def wrapped(*args, **kwargs):
		if not args[0].session.get('cart'):
			session_cart = Cart()
			pcart = pickle.dumps(session_cart)
			request.session['cart'] = pcart
		return view_func(*args, **kwargs)
	return wrapped
