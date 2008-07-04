# -*- coding: utf-8 -*-
'''
    store.views
    ~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

import pickle
from datetime import datetime
from decimal import Decimal
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from store.models import Product, Category, Currency, Order, OrderLine, ORDER_STATUS
from store.decorators import cart_required
from customers.models import CustomerProfile


class Cart(dict):
	"""
	Cart({1, {'id': 1, quantity: 10}})
	"""

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
		total_price = Decimal('0.00')
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

	def set_quantity(self, quantity):
		self['quantity'] = quantity

	def get_price(self):
		price = self.get_product().price * self['quantity']
		return Decimal(str(price))

def cart_debug(request):
	return HttpResponse('%s' % request.session.keys())

def cart_clear(request):
	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear() 
	request.session['cart'] = pickle.dumps(session_cart)
	return HttpResponse('Done')

def cart_set_quantity(request, product_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/store/cart')
		
	product_id = int(product_id)

	try:
		quantity = int(request.POST.get('quantity'))
	except ValueError:
		return HttpResponseRedirect('/store/cart')
		
	if not request.session.get('cart'):
		session_cart = Cart()
		pcart = pickle.dumps(session_cart)
		request.session['cart'] = pcart

	session_cart = pickle.loads(request.session.get('cart'))

	if quantity < 0:
		return HttpResponseRedirect('/store/cart')
	elif quantity == 0:
		del session_cart[product_id]
	else:
		session_cart[product_id]['quantity'] = quantity

	request.session['cart'] = pickle.dumps(session_cart)

	return HttpResponseRedirect('/store/cart')

def product_add(request, slug=''):
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

def set_currency(request):
	if request.method == 'POST':
		currency_code = request.POST.get('currency', None)
		next = request.POST.get('next', None)
	else:
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

def checkout(request, template_name='checkout.html'):
	from customers.forms import CustomerForm

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	if not request.user.is_authenticated():
		request.session['checkout'] = 'True'
		return HttpResponseRedirect('/customer')

	return render_to_response(template_name, context_instance=RequestContext(request))

def submit_order(request, template_name='submit_order.html'):
	from django.core.exceptions import ObjectDoesNotExist

	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse(customer))

	try:
		customer = request.user.get_profile()
	except ObjectDoesNotExist:
		request.user.message_set.create(message=_('%s does not have a customer profile.') % (request.user.username,))
		return HttpResponseRedirect('/store')

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	order = Order(date_time_created=datetime.today(),
		customer=customer,
		currency=request.session['currency'],
		status=ORDER_STATUS[0][0],
		shipping_city=customer.city,
		shipping_country=customer.country,
		)
	order.save()
	for item in session_cart.values():
		order_line = OrderLine.objects.create(
			order=order,
			product=item.get_product(),
			unit_price=item.get_product().price,
			price=item.get_price(),
			quantity=item.get_quantity()
		)
	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear() 
	request.session['cart'] = pickle.dumps(session_cart)

	return HttpResponseRedirect(reverse(success))

def success(request, template_name='order_success.html'):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	return render_to_response(template_name, context_instance=RequestContext(request))

def orders_report(request, template_name='admin/store/orders_report.html'):
	return render_to_response(template_name, {'order_list': Order.objects.all()}, RequestContext(request))


#TODO remove it when we update to 0.97+
def set_language(request):
	"""
	Redirect to a given url while setting the chosen language in the
	session or cookie. The url and the language code need to be
	specified in the request parameters.

	Since this view changes how the user will see the rest of the site, it must
	only be accessed as a POST request. If called as a GET request, it will
	redirect to the page in the request (the 'next' parameter) without changing
	any state.
	"""
	next = request.REQUEST.get('next', None)
	if not next:
		next = request.META.get('HTTP_REFERER', None)
	if not next:
		next = '/'
	response = HttpResponseRedirect(next)
	print 'hello there'
	if request.method == 'POST':
		lang_code = request.POST.get('language', None)
		print lang_code
		#if lang_code and check_for_language(lang_code):
		if lang_code:
			if hasattr(request, 'session'):
				request.session['django_language'] = lang_code
			else:
				response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
	return response
