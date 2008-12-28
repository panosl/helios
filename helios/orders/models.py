from django.db import models


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
