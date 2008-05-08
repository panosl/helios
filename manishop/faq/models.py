# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

from django.db import models
from django.utils.translation import gettext_lazy as _
from faq.conf import settings
import multilingual


class FAQ(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			question = models.CharField(_('question'), maxlength=80)
			answer = models.TextField(_('answer'))
	else:
		question = models.CharField(_('question'), maxlength=80)
		answer = models.TextField(_('answer'))

	creation_date = models.DateField(blank=True, null=True)

	class Meta:
		verbose_name = _('FAQ')
		verbose_name_plural = _('FAQs')

	class Admin:
		pass

	def __str__(self):
		return str(self.question)

	@models.permalink
	def get_absolute_url(self):
		return ('django.views.generic.list_detail.object_detail', None, {
			'id': self.id,
		})
