# -*- coding: utf-8 -*-
'''
    store.templatetags.product
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2009 by Panos Laganakos.
'''

from django.template import Library, Node
from django.template.defaultfilters import stringfilter
from helios.store.models import Product


register = Library()

@register.inclusion_tag('product.html', takes_context=True)
def show_products(context, product_list):
	return {
		'product_list': product_list,
		'currency': context['currency']
	}


@register.filter(name='truncatechars')
@stringfilter
def truncate_chars(value, arg):
	arg = int(arg)
	value = unicode(value)
	if len(value) > arg:
		return u'%s...' % value[:arg]
	else:
		return value
