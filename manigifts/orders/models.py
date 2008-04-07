# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

from django.db import models
from django.utils.translation import gettext_lazy as _
from store.models import Product
from customers.models import CustomerProfile


class Order(models.Model):
	date_time_created = models.DateTimeField(_('Creation Date'))
	customer = models.ForeignKey(CustomerProfile, blank=True, null=True)

	class Meta:
		verbose_name = _('order')
		verbose_name_plural = _('orders')

	class Admin:
		list_display = ['date_time_created']

	def __str__(self):
		return 'Order %s' % self.date_time_created

class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(_('quantity'))

	class Admin:
		pass

	def __str__(self):
		return '%s %s' % (self.quantity, self.product)
