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


def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.
    """
    # avoid a circular import
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}
    for f in opts.fields + opts.many_to_many:
        if not f.editable:
            continue
        if fields and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primry key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.id is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = [obj.id for obj in f.value_from_object(instance)]
        else:
            data[f.name] = f.value_from_object(instance)
    return data

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
		if request.user.is_authenticated():
			customer = CustomerProfile.objects.get(user__exact=request.user)
			initial_data = model_to_dict(customer, fields=['username', 'first_name', 'last_name', 'address'])
		form = CustomerForm(initial=initial_data)

	return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
