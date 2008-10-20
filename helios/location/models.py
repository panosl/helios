# -*- coding: utf-8 -*-
'''
    location.models
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
	name = models.CharField(_('name'), maxlength=45)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural = _('countries')

	class Admin:
		pass

	def __str__(self):
		return self.name
