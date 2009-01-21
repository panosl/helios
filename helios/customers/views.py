# -*- coding: utf-8 -*-
'''
    customers.views
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from helios.customers.forms import CustomerForm, CreateCustomerForm
from helios.customers.models import CustomerProfile
from helios.store.models import Order


def customer(request, template_name='customer.html'):
	if request.method == 'POST':
		form  = CustomerForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['username'],
				form.cleaned_data['email'], form.cleaned_data['password1'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()

			customer = CustomerProfile(user=user, address=form.cleaned_data['address'],
				city=form.cleaned_data['city'], country=form.cleaned_data['country'])
			customer.save()

			#if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			login(request, user)
			request.user.message_set.create(message='Thanks for registering %s!' % (request.user.first_name,))
			if request.session.get('checkout'):
				return HttpResponseRedirect('/store/checkout')
			else:
				return HttpResponseRedirect('/')
	else:
		if request.user.is_authenticated():
			try:
				customer = request.user.get_profile()
				initial_data = {
					'username': customer.user.username,
					'first_name': customer.user.first_name,
					'last_name': customer.user.last_name,
					'email': customer.user.email,
					'address': customer.address,
					'city': customer.city,
					'country': customer.country_id,
				}
				#initial_data = model_to_dict(customer, fields=['username', 'first_name', 'last_name', 'address'])
				form = CustomerForm(initial=initial_data)
			except:
				return HttpResponseRedirect('/')

		else:
			form = CustomerForm()
	return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))


def order_list(request, **kwargs):
	customer = request.user.get_profile()
	return object_list(request, queryset=customer.order_set.all(), **kwargs)
