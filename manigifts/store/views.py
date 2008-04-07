# -*- coding: utf-8 -*-
'''
    store.views
    ~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

import pickle
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import urlresolvers
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from store.models import Product, Category, Currency
from orders.models import Order


class Cart(dict):
	def __init__(self, **products):
		super(Cart, self).__init__(products)

	def add_product(self, product_id, quantity=1):
		# TODO should it raise an exception instead of quantity
		# increase?
		if self.has_key(product_id):
			self[product_id]['quantity'] += quantity
		else:
			self[product_id] = CartLine(id=product_id, quantity=quantity)
	
	def remove_product(self, product_id):
		del self[product_id]

	def get_product_list(self):
		'''Returns the product_list based on the currently stored IDs'''
		product_list = Product.objects.in_bulk(self.keys())
		return product_list.values()

	def get_product_count(self):
		count = 0
		#[(count += product['quantity']) for product in self.itervalues()]
		for product in self.itervalues():
			count += product['quantity']
		return count

	def get_price(self):
		total_price = 0.0
		for cart_line in self.itervalues():
			total_price = total_price + cart_line.get_price()
		return total_price

class CartLine(dict):
	def __init__(self, **line):
		super(CartLine, self).__init__(line)
	
	def get_product(self):
		product = Product.objects.get(id__exact=self['id'])
		return product

	def get_quantity(self):
		return self['quantity']

	def get_price(self):
		price = self.get_product().price * self['quantity']
		return price

def cart_debug(request):
	return HttpResponse('%s' % request.session.keys())

def cart_clear(request):
	if not request.session.get('cart'):
		return HttpResponse('Nothing to clear.')

	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear() 
	request.session['cart'] = pickle.dumps(session_cart)
	return HttpResponse('Done')

def product_add(request, slug=''):
	if not request.session.get('cart'):
		session_cart = Cart()
		pcart = pickle.dumps(session_cart)
		request.session['cart'] = pcart

	session_cart = pickle.loads(request.session.get('cart'))
	
	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		return HttpResponse('That product does not exist.')

	session_cart.add_product(product.id, 1)
	request.session['cart'] = pickle.dumps(session_cart)

        url = request.META.get('HTTP_REFERER', None)
	if url is None:
		url = '/store/products'

	return HttpResponseRedirect(url)

def product_remove(request, slug=''):
	session_cart = pickle.loads(request.session.get('cart'))

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		return HttpResponse('That product does not exist.')

	try:
		session_cart.remove_product(product.id)
	except KeyError:
		return HttpResponse('Does not have one of those!')

	request.session['cart'] = pickle.dumps(session_cart)
	return HttpResponseRedirect('/store/cart')

def category_list(request, category, **kwargs):
	product_list = Product.objects.filter(category__slug__exact=category) #TODO should this change to name, and unslugify it?
	kwargs['extra_context']['category'] = Category.objects.get(slug__exact=category)
	return object_list(request, queryset=product_list, **kwargs)

def checkout(request, template_name='checkout.html'):
	from django.template import RequestContext
	from customers.forms import CustomerForm

	if not request.session['cart']:
		return HttpResponse('No cart amigo...')

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/customer')

	return render_to_response(template_name, context_instance=RequestContext(request))

def submit_order(request, template_name='submit_order.html'):
	if not request.session['cart']:
		return HttpResponse('No cart amigo...')

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/customer')

#def set_currency(request):
#	from store.models import Currency

#	currency_code = request.GET.get('currency', None)
#	next = request.GET.get('next', None)
#	if not next:
#		next = request.META.get('HTTP_REFERER', None)
#	if not next:
#		next = '/'
#	response = HttpResponseRedirect(next)
#	currency = Currency.objects.get(code__exact=request.POST.get('currency', 'DOL'))
#	if currency:
#		if hasattr(request, 'session'):
#			request.session['currency'] = currency
def set_currency(request):
	currency_code = request.GET.get('currency', None)
	next = request.GET.get('next', None)
	if not next:
		next = request.META.get('HTTP_REFERER', None)
	if not next:
		next = '/'
	response = HttpResponseRedirect(next)
	if currency_code:
		if hasattr(request, 'session'):
			request.session['currency'] = Currency.objects.get(code__exact=currency_code)
		else:
			response.set_cookie('currency', currency_code)
	return response
