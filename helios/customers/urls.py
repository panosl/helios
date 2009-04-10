from django.conf.urls.defaults import *
from django.views.generic import list_detail
from helios.customers.views import order_list

urlpatterns = patterns('',
	url(r'^$', 'helios.customers.views.customer',
		name='customer'),
	url(r'^register/$', 'helios.customers.views.customer',
		name='customer-register'),
	(r'^orders/$', order_list, {'template_name': 'customer/orders.html', 'template_object_name': 'order'}),
	url(r'^login/$', 'django.contrib.auth.views.login',
		name='customer-login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',
		name='customer-logout'),
	(r'^reset-password/$', 'django.contrib.auth.views.password_reset'),
)
