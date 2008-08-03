# -*- coding: utf-8 -*-
'''
    store.templatetags.category_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

from django.template import Library, Node
from helios.store.models import Category


register = Library()

@register.inclusion_tag('categories.html')
def show_categories():
	categories = Category.objects.all()
	return {'categories': categories}
