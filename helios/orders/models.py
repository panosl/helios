from django.db import models


ORDER_STATUS = (
	('PENDING', _('Pending')),
	('BILLED', _('Billed')),
	('SHIPPED', _('Shipped')),
)

class Order(models.Model):
	date_time_created = models.DateTimeField(_('creation date'))
	customer = models.ForeignKey(CustomerProfile, blank=True, null=True)
	currency_code = models.CharField(_('code'), maxlength=3, blank=True, null=True)
	currency_factor = models.FloatField(_('factor'), max_digits=10, decimal_places=4, blank=True, null=True)
	status = models.CharField(_('status'), maxlength=10, choices=ORDER_STATUS, blank=True)
	shipping_city = models.CharField(_('city'), maxlength=50, blank=True)
	shipping_country = models.CharField(_('country'), maxlength=50)

	class Meta:
		verbose_name = _('order')
		verbose_name_plural = _('orders')

	class Admin:
		list_display = ['date_time_created', 'customer', 'status']
		list_filter = ('status',)

	def __str__(self):
		return 'Order %s' % self.date_time_created

class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	unit_price = models.FloatField(_('unit price'), max_digits=6, decimal_places=2, blank=True)
	price = models.FloatField(_('line price'), max_digits=6, decimal_places=2, blank=True)
	quantity = models.IntegerField(_('quantity'))

	class Admin:
		pass

	def __str__(self):
		return '%s %s' % (self.quantity, self.product)
