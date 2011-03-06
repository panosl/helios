# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from helios.store.models import Product, ProductImage
from helios.conf import settings
from helios.store.views import category_list


product_dict = {
	'queryset': Product.objects.filter(is_active__exact=True),
	'template_object_name': 'product',
	'extra_context': {'productimage_list': ProductImage.objects.all()},
}

urlpatterns = patterns('helios.store.views',
	(r'^cart/clear/$', 'cart_clear'),
	(r'^cart/debug/$', 'cart_debug'),

	url(r'^cart/set/(?P<product_id>\d+)/$',
		'cart_set_quantity',
		name='store_cart_set_quantity'),
	url(r'^checkout/$',
		'checkout',
		name='store_checkout'),
	url(r'^success/$', 'success',
		name='store_success'),
	url(r'^submit-order/$',
		'submit_order',
		name='store_submit_order'),
	url(r'^products/(?P<slug>[-\w]+)/add/$',
		'product_add',
		name='store_product_add'),
	url(r'^products/(?P<slug>[-\w]+)/remove/$',
		'product_remove',
		name='store_product_remove'),
)

urlpatterns += patterns('',
	url(r'^$',
		direct_to_template,
		{'template': 'home.html'},
		name='store'),

	url(r'^cart/$',
		direct_to_template,
		{'template': 'cart.html'},
		name='store_cart'),

	url(r'^products/(?P<slug>[-\w]+)/$', object_detail,
		dict(product_dict,
		slug_field='slug')),

	url(r'^products/$',
		object_list,
		dict(product_dict,
			paginate_by=settings.PAGINATE_BY),
		name='store_product_list'),

	url(r'^(?P<category>[-\w]+)/$',
		category_list,
		dict(paginate_by=settings.PAGINATE_BY,
			template_object_name='product',
			extra_context={}),
		name='store_category_list'),
)

if settings.USE_PAYPAL:
	urlpatterns += patterns('',
		(r'^paypal/', include('helios.paypal.urls')),
	)
