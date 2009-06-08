# -*- coding: utf-8 -*-
'''
    store.views
    ~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
import pickle
from datetime import datetime
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from helios.store.models import Product, Category, Order, OrderLine, ORDER_STATUS
from helios.store.decorators import cart_required
from helios.customers.models import CustomerProfile
from helios.store.cart import Cart, CartLine


def cart_debug(request):
	return HttpResponse('%s' % request.session.keys())

def cart_clear(request):
	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear() 
	request.session['cart'] = pickle.dumps(session_cart)
	return HttpResponse('Done')

def cart_set_quantity(request, product_id, success_url='/store/cart'):
	if not request.method == 'POST':
		return HttpResponseRedirect(success_url)

	try:
		quantity = int(request.POST.get('quantity'))
	except ValueError:
		return HttpResponseRedirect(success_url)
		
	if not request.session.get('cart'):
		session_cart = Cart()
		pcart = pickle.dumps(session_cart)
		request.session['cart'] = pcart

	session_cart = pickle.loads(request.session.get('cart'))

	product_id = int(product_id)
	items_in_stock = session_cart[product_id].get_product().stock

	if quantity < 0:
		return HttpResponseRedirect(success_url)
	elif quantity == 0 or items_in_stock == 0:
		del session_cart[product_id]
	else:
		if quantity >= items_in_stock:
			session_cart[product_id]['quantity'] = items_in_stock
		else:
			session_cart[product_id]['quantity'] = quantity

	request.session['cart'] = pickle.dumps(session_cart)

	return HttpResponseRedirect(success_url)

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

def checkout(request, template_name='checkout.html'):
	from helios.customers.forms import CustomerForm

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	if not request.user.is_authenticated():
		request.session['checkout'] = 'True'
		return HttpResponseRedirect(reverse('customer-register'))

	return render_to_response(template_name, context_instance=RequestContext(request))

def submit_order(request, template_name='submit_order.html'):
	from django.core.exceptions import ObjectDoesNotExist

	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('customer-register'))

	try:
		customer = request.user.get_profile()
	except ObjectDoesNotExist:
		request.user.message_set.create(message=_(u'%s does not have a customer profile.') % (request.user.username,))
		return HttpResponseRedirect('/store')

	session_cart = pickle.loads(request.session.get('cart'))
	if len(session_cart) == 0:
		return HttpResponseRedirect('/store/cart')

	order = Order.objects.create(
		date_time_created=datetime.today(),
		customer=customer,
		#currency_code=request.session['currency'].code,
		#currency_factor=request.session['currency'].factor,
		status=ORDER_STATUS[0][0],
		shipping_city=customer.city,
		shipping_country=customer.country,
		)

	for cart_line in session_cart.values():
		print cart_line.get_quantity()
		order_line = OrderLine.objects.create(
			order=order,
			product=cart_line.get_product(),
			unit_price=cart_line.get_product().price,
			price=cart_line.get_price(),
			quantity=cart_line.get_quantity()
		)
	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear() 
	request.session['cart'] = pickle.dumps(session_cart)

	return HttpResponseRedirect(reverse(success))

def success(request, template_name='order_success.html'):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	return render_to_response(template_name, context_instance=RequestContext(request))
