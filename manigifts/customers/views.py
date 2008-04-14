# -*- coding: utf-8 -*-
'''
    customers.views
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from customers.forms import CustomerForm, CreateCustomerForm
from customers.models import CustomerProfile


#def customer(request):
#	if request.method == 'POST':
#		form = CustomerForm(request.POST)
#	#if request.user.is_authenticated():
#		#form = CustomerForm(request.user.get_profile())
#	else:
#		form = CustomerForm()

#	return render_to_response('customer.html', {'form': form}, context_instance=RequestContext(request))

def customer(request, template_name='customer.html'):
	if request.method == 'POST':
		form  = CustomerForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(form.clean_data['username'],
				form.clean_data['email'], form.clean_data['password1'])
			user.first_name = form.clean_data['first_name']
			user.last_name = form.clean_data['last_name']
			user.save()

			customer = CustomerProfile(user=user, address=form.clean_data['address'],
				city=form.clean_data['city'], country=form.clean_data['country'])
			customer.save()

			#if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			user = authenticate(username=form.clean_data['username'], password=form.clean_data['password1'])
			login(request, user)
			request.user.message_set.create(message='Thanks for registering %s!' % (request.user.first_name,))
			if request.session['checkout']:
				return HttpResponseRedirect('/store/checkout')
			else:
				return HttpResponseRedirect('/')
	else:
		form = CustomerForm()

	return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
