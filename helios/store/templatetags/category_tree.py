# -*- coding: utf-8 -*-
from django.template import Library, Node
from helios.store.models import Category


register = Library()


@register.inclusion_tag('categories.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}
