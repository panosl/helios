from django import template
from store.models import Currency


register = template.Library()

@register.filter(name='currency')
def set_currency(value, arg):
	#currency = Currency.objects.get(code__exact=arg)
	#return '%s%s' % (currency.symbol, currency.factor * value)
	return Currency.objects.get(code__exact=arg).factor * value
