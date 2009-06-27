from django.db import models
from django.utils.translation import gettext_lazy as _
from helios.customers.models import CustomerProfile
from helios.store.models import Product
from helios.store.conf import settings
if settings.IS_MULTILINGUAL:
	import multilingual


class ShippingMethod(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=80)
		desc = models.TextField(_('description'), blank=True)

	slug = models.SlugField(unique=True, max_length=80)
	cost = models.DecimalField(_('cost'), max_digits=6, decimal_places=2)
	free_limit = models.DecimalField(_('free limit'), max_digits=6, decimal_places=2,
		help_text='Above this price, shipping is for free.')

ORDER_STATUS = (
	('PENDING', _('Pending')),
	('BILLED', _('Billed')),
	('SHIPPED', _('Shipped')),
)

class Order(models.Model):
	date_time_created = models.DateTimeField(_('creation date'))
	customer = models.ForeignKey(CustomerProfile, blank=True, null=True)
	currency_code = models.CharField(_('code'), max_length=3, blank=True, null=True)
	currency_factor = models.DecimalField(_('factor'), max_digits=10, decimal_places=4, blank=True, null=True)
	status = models.CharField(_('status'), max_length=10, choices=ORDER_STATUS, blank=True)
	shipping_city = models.CharField(_('city'), max_length=50, blank=True)
	shipping_country = models.CharField(_('country'), max_length=50)

	class Meta:
		verbose_name = _('order')
		verbose_name_plural = _('orders')

	def __unicode__(self):
		return 'Order %s' % self.date_time_created

class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	unit_price = models.DecimalField(_('unit price'), max_digits=6, decimal_places=2, blank=True)
	price = models.DecimalField(_('line price'), max_digits=6, decimal_places=2, blank=True)
	quantity = models.IntegerField(_('quantity'))

	def __unicode__(self):
		return u'%s %s' % (self.quantity, self.product)
