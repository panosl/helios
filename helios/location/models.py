# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(_('name'), max_length=45)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __unicode__(self):
        return self.name
