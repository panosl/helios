# -*- coding: utf-8 -*-
import pickle
from datetime import datetime
from decimal import Decimal
from django.core.mail import send_mail, mail_managers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list
from helios.conf import settings
from helios.orders.models import OrderStatus, Order, OrderLine, PaymentOption
from helios.orders.forms import OrderForm
from helios.shipping.models import ShippingMethodRegions
from helios.store.models import Product, Category, PaymentOption
from helios.store.forms import PaymentForm
from helios.store.cart import Cart
from helios.store.decorators import cart_required
if settings.USE_PAYPAL:
	from helios.paypal.views import *


def cart_debug(request):
	return HttpResponse('%s' % request.session.items())


def cart_clear(request):
	session_cart = pickle.loads(request.session.get('cart'))
	session_cart.clear()
	request.session['cart'] = session_cart.dump()
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
		pcart = session_cart.dump()
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

	request.session['cart'] = session_cart.dump()

	return HttpResponseRedirect(success_url)


def product_add(request, slug=''):
	try:
		session_cart = pickle.loads(request.session.get('cart'))
	except TypeError:
		return HttpResponse('Your browser does not support sessions.')

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		return HttpResponse('That product does not exist.')

	session_cart.add_product(product.id, 1)
	request.session['cart'] = session_cart.dump()

	url = request.META.get('HTTP_REFERER', None)
	if url is None:
		#url = '/store/products'
		url = reverse('store_product_list')

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

	request.session['cart'] = session_cart.dump()
	return HttpResponseRedirect(reverse('store_cart'))


def category_list(request, category, **kwargs):
	product_list = Product.objects.filter(category__slug__exact=category)
	kwargs['extra_context']['category'] = Category.objects.get(slug__exact=category)
	return object_list(request, queryset=product_list, **kwargs)


@cart_required
def checkout(request, template_name='checkout.html'):
	session_cart = pickle.loads(request.session.get('cart'))

	if not request.user.is_authenticated():
		request.session['checkout'] = 'True'
		return HttpResponseRedirect(reverse('customer-register'))

	customer = request.user.customer
	order_total = session_cart.get_price()

	if not customer.country.shippingregion_set.all():
		return HttpResponseRedirect(reverse('store_unshippable'))

	if request.method == 'POST':
		#shipping_form = OrderForm(customer, request.POST,
			#initial={'shipping_choice': request.POST['shipping_choice']})
		shipping_form = OrderForm(customer, request.POST)
		payment_form = PaymentForm(request.POST)

		if shipping_form.is_valid():
			shipping_choice = shipping_form.cleaned_data['shipping_choice']
			order_total += Decimal(shipping_choice.cost)
			request.session['shipping_choice'] = shipping_choice.id

		if payment_form.is_valid():
			payment_option = payment_form.cleaned_data['payment_option']
			request.session['payment_option'] = payment_option.id

		if payment_form.is_valid() and shipping_form.is_valid():
			return HttpResponseRedirect(reverse(submit_order))
	else:
		shipping_form = OrderForm(customer)
		payment_form = PaymentForm()

	return render_to_response(template_name,
		{
			'customer': customer,
			'shipping_form': shipping_form,
			'payment_form': payment_form,
			'order_total': order_total,
		},
		context_instance=RequestContext(request))


@login_required
def unshippable(request, template_name='store/unshippable.html'):
	customer = request.user.customer

	if customer.country.shippingregion_set.all():
		url = request.META.get('HTTP_REFERER', None)
		if url is None:
			url = reverse('store')
		return HttpResponseRedirect(url)
	return render_to_response(template_name, {
			'customer': request.user.customer,
	},
	context_instance=RequestContext(request))


@cart_required
@login_required
def submit_order(request, template_name='checkout.html'):
	try:
		shipping_choice = ShippingMethodRegions.objects.get(pk=request.session['shipping_choice'])
	except KeyError:
		request.user.message_set.create(message=_(u'%s you haven\'t chosen a shipping method.') % (request.user.username,))
		return HttpResponseRedirect(reverse('store_checkout'))

	try:
		payment_option = PaymentOption.objects.get(pk=request.session['payment_option'])
	except KeyError:
		request.user.message_set.create(message=_(u'%s you haven\'t chosen a payment option.') % (request.user.username,))
		return HttpResponseRedirect(reverse('store_checkout'))

	customer = request.user.customer
	session_cart = pickle.loads(request.session.get('cart'))

	if payment_option.slug == 'paypal':
		return HttpResponseRedirect(reverse(paypal_purchase))

	order_dict = {
		'date_time_created': datetime.today(),
		'customer': customer,
		'status': OrderStatus.objects.get(slug__exact='pending'),
		'shipping_city': customer.city,
		'shipping_country': customer.country,
		'shipping_choice': shipping_choice,
		'payment_option': payment_option
	}
	if settings.HAS_CURRENCIES:
		order_dict['currency_code'] = request.session['currency'].code,
		order_dict['currency_factor'] = request.session['currency'].factor,
	order = Order.objects.create(**order_dict)

	for cart_line in session_cart.values():
		order_line = OrderLine.objects.create(
			order=order,
			product=cart_line.get_product(),
			unit_price=cart_line.get_product().price,
			price=cart_line.get_price(),
			quantity=cart_line.get_quantity()
		)
	session_cart.clear()
	request.session['cart'] = session_cart.dump()

	#TODO maybe turn this into a signal
	subject = render_to_string('store/order_subject.txt', {'order': order})

	send_mail(''.join(subject.splitlines()), render_to_string('store/order.txt', {'order': order, 'customer': customer, 'country': customer.country }), 'noreply@holabyolga.gr', [customer.email])
	mail_managers(''.join(subject.splitlines()), render_to_string('store/order.txt', {'order': order, 'customer': customer, 'country': customer.country }), fail_silently=False)

	return HttpResponseRedirect(reverse(success))


@login_required
def success(request, template_name='order_success.html'):
	return render_to_response(template_name, context_instance=RequestContext(request))
