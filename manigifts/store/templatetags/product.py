# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

from django.template import Library, Node
from store.models import Product


register = Library()

@register.inclusion_tag('product.html', takes_context=True)
def show_products(context, product_list):
	return {
		'product_list': product_list,
		'currency': context['currency']
	}
