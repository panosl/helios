# -*- coding: utf-8 -*-
'''
    store.templatetags.product
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

from django.template import Library, Node
from helios.store.models import Product


register = Library()

@register.inclusion_tag('product.html', takes_context=True)
def show_products(context, product_list):
	return {
		'product_list': product_list,
		'currency': context['currency']
	}
