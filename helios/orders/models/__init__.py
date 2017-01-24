from django.db import models
from django.utils.translation import ugettext_lazy as _

from helios.customers.models import BaseCustomer
from helios.store.models import BaseProduct


class BaseOrder(models.Model):
    customer = models.ForeignKey(BaseCustomer, blank=True, null=True, verbose_name=_('customer'))
    created_at = models.DateTimeField(_('Created at'))
    updated_at = models.DateTimeField(_('Updated at'))

    class Meta:
        abstract = True


class BaseOrderLine(models.Model):
    order = models.ForeignKey(BaseOrder, verbose_name=_('order'))
    product = models.ForeignKey(BaseProduct, verbose_name=_('product'))
    unit_price = models.DecimalField(_('unit price'), max_digits=6, decimal_places=2, blank=True)
    price = models.DecimalField(_('line price'), max_digits=6, decimal_places=2, blank=True)
    quantity = models.IntegerField(_('quantity'))

    class Meta:
        abstract = True
        verbose_name = _('order line')
        verbose_name_plural = _('order lines')

    def __unicode__(self):
        return u'%s %s' % (self.quantity, self.product)
