# -*- coding: utf-8 -*-
import pickle
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def cart_required(view_func):
	def wrapped(*args, **kwargs):
		try:
			session_cart = pickle.loads(args[0].session.get('cart'))
		except:
			pass

		if len(session_cart) == 0:
			return HttpResponseRedirect(reverse('store_cart'))
		else:
			return view_func(*args, **kwargs)
	return wrapped
