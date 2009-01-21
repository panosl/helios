# -*- coding: utf-8 -*-
'''
    store.models
    ~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
import os
import Image
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from helios.customers.models import CustomerProfile
from helios.location.models import Country
from helios.store.conf import settings
if settings.IS_MULTILINGUAL:
	import multilingual


class Currency(models.Model):
	code = models.CharField(_('code'), max_length=3)
	name = models.CharField(_('name'), max_length=25)
	symbol = models.CharField(_('symbol'), max_length=1)
	factor = models.DecimalField(_('factor'), max_digits=10, decimal_places=4,
		help_text=_('Specifies the difference of the currency to Euro.'))

	class Meta:
		verbose_name = _('currency')
		verbose_name_plural = _('currencies')

	def __unicode__(self):
		return self.code

class Category(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=50)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=50)
		desc = models.TextField(_('description'), blank=True)

	slug = models.SlugField(max_length=50, unique=True)
	parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set')

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')

	def __unicode__(self):
		pname = u''
		if self.parent is not None:
			pname = unicode(self.parent) + u': '
			return pname + self.name
		else:
			return self.name

	
	def get_absolute_url(self):
		return '/store/' + self.slug

	#@models.permalink
	#def get_absolute_url(self):
	#	return('category_list', (), {
	#		#'slug': self.slug,
	#	})

class ActiveProductManager(models.Manager):
	def get_query_set(self):
		return super(ActiveProductManager).get_query_set().filter(is_active=True)

class Product(models.Model):

	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), max_length=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), max_length=80)
		desc = models.TextField(_('description'), blank=True)

	slug = models.SlugField(unique=True, max_length=80)
	category = models.ForeignKey(Category, blank=True, null=True)
	date_added = models.DateField(auto_now_add=True)
	is_active = models.BooleanField(_('Is product active?'), default=True,
		help_text=_('Determines if the product will appear in the store.'))
	stock = models.IntegerField(_('Items in stock'), default=0)
	weight = models.PositiveIntegerField(_('weight'), default=0,
		help_text=_('Defined in Kilograms.'))
	price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)

	class Meta:
		verbose_name = _('product')
		verbose_name_plural = _('products')
		ordering = ['-date_added']

	def __unicode__(self):
		return self.name

	@models.permalink	
	def get_absolute_url(self):
		return ('django.views.generic.list_detail.object_detail', (), {
			'slug': self.slug,
		})

	def get_images(self):
		images = self.productimage_set.all()
		return images

	#TODO
	#def get_price()

class ProductImage(models.Model):
	product = models.ForeignKey(Product, null=True, blank=True)
	picture = models.ImageField(_('picture'), upload_to='./product_images')
	suffix = '_thumbnail.jpg'

	class Meta:
		verbose_name = _('product image')
		verbose_name_plural= _('product images')

	def __unicode__(self):
		return str(self.picture)


	def _make_thumbnail(self):
		thumbnail = Image.open(self.picture.path)
		thumbnail.thumbnail((256, 256), Image.ANTIALIAS)
		thumbnail = thumbnail.crop((0, 0, 190, 190))
		thumbnail.save(os.path.splitext(self.picture.path)[0] + self.suffix, 'JPEG')
	
	def _get_thumbnail(self):
		return os.path.splitext(self.picture.url)[0] + self.suffix
	thumbnail = property(_get_thumbnail)

	def save(self):
		super(ProductImage, self).save()
		self._make_thumbnail()

	def delete(self):
		try:
			os.remove(self.picture.path)
		except OSError:
			pass	
		try:
			os.remove(os.path.splitext(self.picture.path)[0] + self.suffix)
		except OSError:
			pass
		super(ProductImage, self).delete()

ORDER_STATUS = (
	('PENDING', _('Pending')),
	('BILLED', _('Billed')),
	('SHIPPED', _('Shipped')),
)

class Order(models.Model):
	date_time_created = models.DateTimeField(_('Creation Date'))
	customer = models.ForeignKey(CustomerProfile, blank=True, null=True)
	currency_code = models.CharField(_('currency code'), max_length=3, blank=True, null=True)
	currency_factor = models.DecimalField(_('currency factor'), max_digits=10, decimal_places=4, blank=True, null=True)
	status = models.CharField(max_length=10, choices=ORDER_STATUS, blank=True)
	shipping_city = models.CharField(_('City'), max_length=50, blank=True)
	shipping_country = models.ForeignKey(Country, blank=True)

	class Meta:
		verbose_name = _('order')
		verbose_name_plural = _('orders')

	def __unicode__(self):
		return u'Order %s' % self.date_time_created

class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	unit_price = models.DecimalField(_('unit price'), max_digits=6, decimal_places=2, blank=True)
	price = models.DecimalField(_('line price'), max_digits=6, decimal_places=2, blank=True)
	quantity = models.IntegerField(_('quantity'))

	def __unicode__(self):
		return u'%s %s' % (self.quantity, self.product)
