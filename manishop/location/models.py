# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
	name = models.CharField(_('name'), maxlength=35)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural = _('countries')

	class Admin:
		pass

	def __str__(self):
		return self.name
