# -*- coding: utf-8 -*-
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


@register.filter(name='legacy_truncatechars')
@stringfilter
def truncate_chars(value, arg):
    print 'fuck you'
    arg = int(arg)
    value = unicode(value)
    if len(value) > arg:
        return u'%s...' % value[:arg]
    else:
        return value


@register.filter(name='splitfirstline')
@stringfilter
def split_first_line(value, arg):
    arg = int(arg)
    value = unicode(value).split('\n', 1)
    if arg == 0:
        return value[0]
    elif arg == 1:
        try:
            return value[1]
        except IndexError:
            return ''
