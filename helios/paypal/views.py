# -*- coding: utf-8 -*-
import pickle
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from helios.paypal.forms import MyPayPalForm
from helios.store.decorators import cart_required


@cart_required
@login_required
def paypal_purchase(request, template_name='paypal/payment.html'):
	try:
		shipping_choice = request.session['shipping_choice']
	except KeyError:
		request.user.message_set.create(message=_(u'%s you haven\'t chosen a shipping method.') % (request.user.username,))
		return HttpResponseRedirect(reverse('store_checkout'))

	session_cart = pickle.loads(request.session.get('cart'))
	customer = request.user.customer
	order_total = session_cart.get_price() + request.session['shipping_choice'].cost

	paypal_dict = {
		'business': 'panos_1251033497_biz@phaethon-designs.gr',
		'amount': order_total,
		'item_name': 'manishop purchase',
		#'invoice': 'unique-invoice-id',
		'notify_url': 'http://79.107.108.6:8000/store/ppp/',
		'return_url': 'http://79.107.108.6:8000/store/ppp/',
		'cancel_return': 'http://www.example.com/your-cancel-location/',
		'no_shipping': MyPayPalForm.SHIPPING_CHOICES[1][0],
		'address_override': 1,
		'first_name': customer.user.first_name,
		'last_name': customer.user.last_name,
		'address1': customer.address,
		'city': customer.city,
		'postal_code': customer.postal_code,
		'country': customer.country,
		'email': customer.user.email,
	}

	if settings.HAS_CURRENCIES:
		paypal_dict['currency_code'] = request.session['currency'].code

	#form = PayPalPaymentsForm(initial=paypal_dict)
	form = MyPayPalForm(initial=paypal_dict)

	return render_to_response(template_name,
		{'form': form},
		context_instance=RequestContext(request))
