# -*- coding: utf-8 -*-
'''
    store.context_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

import pickle
from store.models import Currency
from store.views import Cart, CartLine


def cart(request):
	if not request.session.get('cart'):
		cart = Cart()
		request.session['cart'] = pickle.dumps(cart)
	
	return {'cart': pickle.loads(request.session['cart'])}

def currency(request):
	currencies = Currency.objects.all()
	if not request.session.get('currency'):
		request.session['currency'] = Currency.objects.get(code__exact='EUR')

	return {
		'CURRENCIES': currencies,
		'currency': request.session['currency']
	}
