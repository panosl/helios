# -*- coding: utf-8 -*-
'''
    customers.models
    ~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from helios.location.models import Country


class CustomerProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	phone = models.CharField(_('phone number'), max_length=30, blank=True)
	fax = models.CharField(_('Fax'), max_length=30, blank=True)
	address = models.TextField(_('address'), blank=True)
	postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
	city = models.CharField(_('city'), max_length=50, blank=True)
	country = models.ForeignKey(Country)

	class meta:
		verbose_name = _('customer profile')
		verbose_name_plural = _('customer profiles')

	def __unicode__(self):
		return u'%s (%s)' % (self.user.get_full_name(), self.user.email)
