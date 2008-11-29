# -*- coding: utf-8 -*-
'''
    store.urls
    ~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from helios.store.models import Product, ProductImage, Category
from helios.store.conf import settings
from helios.store.views import category_list


product_dict = {
	'queryset': Product.objects.all(), # We retrieve all of them and decide on the template
	'template_object_name': 'product',
	'extra_context': {'productimage_list': ProductImage.objects.all()},
}

urlpatterns = patterns('helios.store.views',
	(r'^setcurrency/$', 'set_currency'),
	(r'^setlang/$', 'set_language'),
	(r'^cart/clear/$', 'cart_clear'),
	(r'^cart/set/(?P<product_id>\d+)/$', 'cart_set_quantity'),
	(r'^cart/debug/$', 'cart_debug'),
	(r'^checkout/$', 'checkout'),
	(r'^success/$', 'success'),
	(r'^submit-order/$', 'submit_order'),
	(r'^products/(?P<slug>[-\w]+)/add/$', 'product_add'),
	(r'^products/(?P<slug>[-\w]+)/remove/$', 'product_remove'),
)

urlpatterns += patterns('',
	(r'^$', direct_to_template, {'template': 'home.html'}),
	(r'^cart/$', direct_to_template, {'template': 'cart.html'}),
	(r'^products/(?P<slug>[-\w]+)/$', object_detail, dict(product_dict, slug_field='slug')),
	(r'^products/$', object_list, dict(product_dict, paginate_by=settings.PAGINATE_BY)),
	(r'^(?P<category>[-\w]+)/$', category_list, dict(paginate_by=settings.PAGINATE_BY, template_object_name='product', extra_context={})),
)
