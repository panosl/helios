from django.db import models
from django.utils.translation import ugettext_lazy as _
from helios.location.models import Country
from helios.conf import settings
if settings.IS_MULTILINGUAL:
	import multilingual

class Shipper(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=80)
		desc = models.TextField(_('description'), blank=True)
	slug = models.SlugField(unique=True, max_length=80)

	class Meta:
		verbose_name = _('shipper')
		verbose_name_plural = _('shippers')

	def __unicode__(self):
		return self.name

class ShippingRegion(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=80)
		desc = models.TextField(_('description'), blank=True)
	slug = models.SlugField(unique=True, max_length=80)
	countries = models.ManyToManyField(Country)
	shipper = models.ForeignKey(Shipper)

	class Meta:
		verbose_name = _('shipping region')
		verbose_name_plural = _('shipping regions')

	def __unicode__(self):
		return u'%s-%s' % (self.shipper, self.name)

class ShippingMethod(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=80)
		desc = models.TextField(_('description'), blank=True)
	slug = models.SlugField(unique=True, max_length=80)
	shipper = models.ForeignKey(Shipper)
	shipping_regions = models.ManyToManyField(ShippingRegion, through='ShippingMethodRegions')

	class Meta:
		verbose_name = _('shipping method')
		verbose_name_plural = _('shipping methods')

	def _cost(self):
		pass

	def __unicode__(self):
		return self.name

class ShippingMethodRegions(models.Model):
	region = models.ForeignKey(ShippingRegion)
	method = models.ForeignKey(ShippingMethod)
	cost = models.DecimalField(_('price'), max_digits=6, decimal_places=2)

	class Meta:
		verbose_name_plural = _('shipping method regions')
	
	def __unicode__(self):
		return u'%s-%s' % (self.region, self.method,)
