# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from helios.store.models import Product, ProductImage
from helios.conf import settings
from helios.store.views import category_list, collection_list, ProductDetail


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
    url(r'^unshippable/$',
        'unshippable',
        name='store_unshippable'),
)

urlpatterns += patterns('',
    url(r'^cart/$',
        direct_to_template,
        {'template': 'cart.html'},
        name='store_cart'
    ),
    url(r'^products/(?P<slug>[-\w]+)/$', ProductDetail.as_view(),
        name='store_product_detail'
    ),
    url(r'^products/$',
        object_list,
        dict(product_dict,
            paginate_by=settings.PAGINATE_BY),
        name='store_product_list'
    ),
    url(r'^collections/(?P<collection>[-\w]+)/$',
        collection_list,
        dict(paginate_by=settings.PAGINATE_BY,
            template_object_name='product',
            extra_context={}),
        name='store_collection_list'
    ),
    url(r'^(?P<category>[-\w]+)/$',
        category_list,
        dict(paginate_by=settings.PAGINATE_BY,
            template_object_name='product',
            extra_context={}),
        name='store_category_list'
    ),
)
