from django.db import models
from django.utils.translation import ugettext_lazy as _

from helios.store.models import Category


class CategoryPercentageDiscount(models.Model):
    category = models.OneToOneField(Category)
    discount = models.DecimalField(_('discount'), max_digits=5, decimal_places=2)

    def __unicode__(self):
        return u'%s %s%%' % (self.category, self.discount,)
