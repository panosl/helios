from django.db import models
from django.utils.translation import ugettext_lazy as _

from helios.customers.models import CustomerProfile
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


class BaseOrder(models.Model):
    customer = models.ForeignKey(CustomerProfile, blank=True, null=True, verbose_name=_('customer'))
    created_at = models.DateTimeField(_('Created at'))
    updated_at = models.DateTimeField(_('Updated at'))

    class Meta:
        abstract = True


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
        ordering = ['-date_time_created']

    def __unicode__(self):
        return u'Order %s' % self.created_at


class BaseOrderLine(models.Model):
    order = models.ForeignKey(BaseOrder, verbose_name=_('order'))
    product = models.ForeignKey(Product, verbose_name=_('product'))
    unit_price = models.DecimalField(_('unit price'), max_digits=6, decimal_places=2, blank=True)
    price = models.DecimalField(_('line price'), max_digits=6, decimal_places=2, blank=True)
    quantity = models.IntegerField(_('quantity'))

    class Meta:
        abstract = True
        verbose_name = _('order line')
        verbose_name_plural = _('order lines')

    def __unicode__(self):
        return u'%s %s' % (self.quantity, self.product)


class OrderLine(BaseOrderLine):
    pass
