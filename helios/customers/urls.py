from django.conf.urls.defaults import *
from django.views.generic import list_detail
from helios.customers.views import order_list

urlpatterns = patterns('',
	url(r'^$',
		'helios.customers.views.customer',
		name='customer'),
	url(r'^register/$',
		'helios.customers.views.register',
		name='customer-register'),
	url(r'^orders/$',
		order_list, {
			'template_name': 'customer/orders.html',
			'template_object_name': 'order'},
		name='customer-orders'),
	url(r'^login/$',
		'django.contrib.auth.views.login',
		name='customer-login'),
	url(r'^logout/$',
		'django.contrib.auth.views.logout', {
			'template_name': 'customer/logged_out.html',
		},
		name='customer-logout'),
	url(r'^reset-password/$',
		'django.contrib.auth.views.password_reset',
		name='customer-reset-password'),
	url(r'^reset-password-done/$',
		'django.contrib.auth.views.password_reset_done',
		name='customer-reset-password-done'),
)
