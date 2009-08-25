# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from helios.location.models import Country
from helios.shipping.models import *


class CustomerProfile(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(_('phone number'), max_length=30, blank=True)
	fax = models.CharField(_('Fax'), max_length=30, blank=True)
	address = models.TextField(_('address'), blank=True)
	postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
	city = models.CharField(_('city'), max_length=50, blank=True)
	country = models.ForeignKey(Country, blank=True, null=True)

	class meta:
		verbose_name = _('customer profile')
		verbose_name_plural = _('customer profiles')

	def __unicode__(self):
		return u'%s' % (self.user.get_full_name())

	def shipping_methods(self):
		methods = [region.shippingmethodregions_set.all() for region in self.country.shippingregion_set.all()]
		methods = [method[0] for method in methods]
		return methods

	@property
	def first_name(self):
		return self.user.first_name

	@property
	def last_name(self):
		return self.user.last_name

	def get_full_name(self):
		return self.user.get_full_name()
	
	@property
	def email(self):
		return self.user.email
	

User.customer = property(lambda u: CustomerProfile.objects.get_or_create(user=u, \
				defaults={'country': Country.objects.get(pk=1)})[0])
