from django.db import models
from django.utils.translation import ugettext_lazy as _

from helios.location.models import Country
from helios.shipping.models import ShippingMethodRegions
from helios.store.models import Product
from helios.payment.models import PaymentOption


class OrderStatus(models.Model):
    name = models.CharField(_('name'), max_length=50)
    desc = models.TextField(_('description'), blank=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = _('order status')
        verbose_name_plural = _('order statuses')

    def __unicode__(self):
        return self.name

class Order(BaseOrder):
    if settings.HAS_CURRENCIES:
        currency_code = models.CharField(_('currency code'), max_length=3, blank=True, null=True)
        currency_factor = models.DecimalField(_('currency factor'), max_digits=10, decimal_places=4, blank=True, null=True)
    status = models.ForeignKey(OrderStatus, blank=True, null=True)
    shipping_city = models.CharField(_('City'), max_length=50, blank=True)
    shipping_country = models.ForeignKey(Country, blank=True, null=True, verbose_name='shipping country')
    shipping_choice = models.ForeignKey(ShippingMethodRegions, blank=True, null=True)
    payment_option = models.ForeignKey(PaymentOption, blank=True, null=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']

    def __unicode__(self):
        return u'Order %s' % self.created_at


class OrderLine(BaseOrderLine):
    pass
