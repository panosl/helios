# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

from django.template import Library, Node
from store.models import Category


register = Library()

@register.inclusion_tag('categories.html')
def show_categories():
	categories = Category.objects.all()
	return {'categories': categories}
