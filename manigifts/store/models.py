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
from customers.models import CustomerProfile
from store.conf import settings
if settings.IS_MULTILINGUAL:
	import multilingual


class Currency(models.Model):
	code = models.CharField(_('code'), maxlength=3)
	name = models.CharField(_('name'), maxlength=25)
	symbol = models.CharField(_('symbol'), maxlength=1)
	factor = models.FloatField(_('factor'), max_digits=10, decimal_places=4,
		help_text=_('Specifies the difference of the currency to Euro.'))

	class Meta:
		verbose_name = _('currency')
		verbose_name_plural = _('currencies')

	class Admin:
		list_display = ('code', 'name', 'symbol', 'factor')
		list_display_links = ('name',)

	def __str__(self):
		return self.code

class Category(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(maxlength=50)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(maxlength=50)
		desc = models.TextField(_('description'), blank=True)

	slug = models.SlugField(prepopulate_from=('name',))
	parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')

	class Admin:
		list_display = ('name', 'desc')
		ordering = ['name']

	def __str__(self):
		pname = ''
		if self.parent is not None:
			pname = str(self.parent) + ': '
			return pname + self.name
		return self.name

	def get_absolute_url(self):
		return '/store/' + self.slug

class ActiveProductManager(models.Manager):
	def get_query_set(self):
		return super(ActiveProductManager).get_query_set().filter(is_active=True)

class Product(models.Model):
	if settings.IS_MULTILINGUAL:
		class Translation(multilingual.Translation):
			name = models.CharField(_('name'), maxlength=80)
			desc = models.TextField(_('description'), blank=True)
	else:
		name = models.CharField(_('name'), maxlength=80)
		desc = models.TextField(_('description'), blank=True)

	slug = models.SlugField(unique=True, prepopulate_from=('producttranslation.0.name',))
	category = models.ForeignKey(Category, blank=True, null=True)
	date_added = models.DateField(auto_now_add=True)
	is_active = models.BooleanField(_('Is product active?'), default=True,
		help_text=_('Determines if the product will appear in the store.'))
	stock = models.IntegerField(_('Items in stock'), default=0)
	weight = models.PositiveIntegerField(_('weight'), default=0,
		help_text=_('Defined in Kilograms.'))
	price = models.FloatField(_('price'), max_digits=6, decimal_places=2)

	class Meta:
		verbose_name = _('product')
		verbose_name_plural = _('products')
		ordering = ['-date_added']

	class Admin:
		list_display = ('name', 'price', 'stock')
		list_filter = ('category',)
		search_fields = ['slug', 'name']

	def __str__(self):
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

	class Meta:
		verbose_name = _('product image')
		verbose_name_plural= _('product images')

	class Admin:
		list_display = ['picture', 'product']

	def __str__(self):
		return str(self.picture)

	def _make_thumbnail(self):
		thumbnail = Image.open(self.get_picture_filename())
		thumbnail.thumbnail((256, 256), Image.ANTIALIAS)
		thumbnail = thumbnail.crop((0, 0, 190, 190))
		thumbnail.save(os.path.splitext(self.get_picture_filename())[0] + '_thumbnail.jpg', 'JPEG')
	
	def _get_thumbnail(self):
		return os.path.splitext(self.get_picture_url())[0] + '_thumbnail.jpg'
	thumbnail = property(_get_thumbnail)

	def save(self):
		super(ProductImage, self).save()
		self._make_thumbnail()

	def delete(self):
		try:
			os.remove(self.get_picture_filename())
		except OSError:
			pass	
		try:
			os.remove(os.path.splitext(self.get_picture_filename())[0] + '_thumbnail.jpg')
		except OSError:
			pass
		super(ProductImage, self).delete()

class Order(models.Model):
	date_time_created = models.DateTimeField(_('Creation Date'))
	customer = models.ForeignKey(CustomerProfile, blank=True, null=True)

	class Meta:
		verbose_name = _('order')
		verbose_name_plural = _('orders')

	class Admin:
		list_display = ['date_time_created']

	def __str__(self):
		return 'Order %s' % self.date_time_created

class OrderLine(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	#TODO
	quantity = models.IntegerField(_('quantity'))

	class Admin:
		pass

	def __str__(self):
		return '%s %s' % (self.quantity, self.product)
