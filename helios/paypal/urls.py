# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from helios.paypal.views import paypal_purchase


urlpatterns = patterns('',
	(r'^paypal/', paypal_purchase),
	(r'^$', include('paypal.standard.ipn.urls')),
)

