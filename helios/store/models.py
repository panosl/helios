import os
from decimal import *

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from helios.conf import settings
if settings.IS_MULTILINGUAL:
    import multilingual


class Tax(models.Model):
    if settings.IS_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(_('name'), max_length=80)
            desc = models.TextField(_('description'), blank=True)
    else:
        name = models.CharField(_('name'), max_length=80)
        desc = models.TextField(_('description'), blank=True)

    slug = models.SlugField(unique=True, max_length=80)
    rate = models.DecimalField(_('tax rate'), max_digits=4, decimal_places=2,
        default=19.00)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The tax will be available in the store.'))

    class Meta:
        verbose_name = _('tax')
        verbose_name_plural = _('taxes')
        pass

    def __unicode__(self):
        return self.name

    def _get_factor(self):
        """Returns the factor depending on the tax rate."""
        return (self.rate / Decimal('100.00')) + Decimal('1.00')
    factor = property(_get_factor)


class CategoryManager(models.Manager):
    def get_root_nodes(self):
        '''return all root node, aka nodes that don\'t have any parent categories'''
        return super(CategoryManager, self).get_queryset().filter(parent=None)


class Category(models.Model):
    if settings.IS_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(_('name'), max_length=50)
            desc = models.TextField(_('description'), blank=True)
    else:
        name = models.CharField(_('name'), max_length=50)
        desc = models.TextField(_('description'), blank=True)

    slug = models.SlugField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_set')

    objects = CategoryManager()

    class Meta:
        ordering = ['name']
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
        #return('helios.store.views.category_list', (), {
        return('store_category_list', (), {
            'category': self.slug,
        })

    def get_children(self):
        return self.child_set.all()

    def is_root_node(self):
        return True if self.parent is None else False


if settings.IS_MULTILINGUAL:
    class ActiveProductManager(multilingual.Manager):
        def get_queryset(self):
            return super(ActiveProductManager).get_queryset().filter(is_active=True)


class BaseProduct(models.Model):
    name = models.CharField(_('name'), max_length=80)
    slug = models.SlugField(unique=True, max_length=80)
    desc = models.TextField(_('description'), blank=True)
    date_added = models.DateField(_('date added'), auto_now_add=True)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The product will appear in the store.'))
    base_price = models.DecimalField(_('base price'), max_digits=6, decimal_places=2)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('store_product_detail', (), {
            'slug': self.slug,
        })



class Product(BaseProduct):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('category'))
    is_featured = models.BooleanField(_('featured'), default=False,
        help_text=_('The product will be featured on the front page.'))
    stock = models.IntegerField(_('stock'), default=0,
        help_text=_('Number of items in stock.'))
    weight = models.PositiveIntegerField(_('weight'), default=0,
        help_text=_('Defined in kilograms.'))
    taxes = models.ManyToManyField(Tax, blank=True, verbose_name=_('taxes'))

    #objects = ActiveProductManager()

    class Meta(BaseProduct.Meta):
        abstract = False
        verbose_name = _('product')
        verbose_name_plural = _('products')
        if not settings.IS_MULTILINGUAL:
            # This will not work for multilingual right now
            ordering = ['-is_featured', '-last_modified']

    def __unicode__(self):
        return self.name or ''

    def get_images(self):
        images = self.productimage_set.all()
        return images

    def _get_images(self):
        images = self.productimage_set.all()
        return images
    images = property(_get_images)

    def _get_price(self):
        tax_factors = [tax.factor for tax in self.taxes.all()]
        taxed_product = (self.base_price * reduce(lambda x, y: x * y, tax_factors, 1)).quantize(Decimal('.01'), rounding=ROUND_UP)
        return taxed_product

    def _get_discounted_price(self):
        tax_factors = [tax.factor for tax in self.taxes.all()]
        taxed_product = (self.base_price * reduce(lambda x, y: x * y, tax_factors, 1)).quantize(Decimal('.01'), rounding=ROUND_UP)
        if self.category.categorypercentagediscount:
            category_discount = Decimal(self.category.categorypercentagediscount.discount)/Decimal('100.0')
            return taxed_product - (taxed_product * category_discount).quantize(Decimal('.01'), rounding=ROUND_UP)

        else:
            return taxed_product


    def has_discount(self):
        if self.category and self.category.categorypercentagediscount:
            return True
        else:
            return False

    price = property(_get_price)
    discounted_price = property(_get_discounted_price)


class BaseProductImage(models.Model):
    picture = models.ImageField(_('picture'), upload_to='./product_images')
    list_position = models.PositiveIntegerField(_('list position'), default=1)
    suffix = '_thumbnail.jpg'

    class Meta:
        abstract = True
        ordering = ['list_position']
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    def __unicode__(self):
        return u'%s' % (self.picture,)

    def delete(self):
        try:
            os.remove(self.picture.path)
        except OSError:
            pass
        try:
            os.remove(os.path.splitext(self.picture.path)[0] + self.suffix)
        except OSError:
            pass
        super(BaseProductImage, self).delete()


class ProductImage(BaseProductImage):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('product'))


class Collection(models.Model):
    if settings.IS_MULTILINGUAL:
        class Translation(multilingual.Translation):
            name = models.CharField(_('name'), max_length=80)
            desc = models.TextField(_('description'), blank=True)
    else:
        name = models.CharField(_('name'), max_length=80)
        desc = models.TextField(_('description'), blank=True)

    slug = models.SlugField(unique=True, max_length=80)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The collection will be available in the store.'))
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

    def __unicode__(self):
        return self.name or ''

    def get_absolute_url(self):
        return('store_collection_list', (), {
            'collection': self.slug,
        })


#try:
#    from paypal.standard.ipn.signals import payment_was_successful
#    def paypal_successful(sender, **kwargs):
#        ipn_obj = sender
#    payment_was_successful.connect(paypal_successful)
#except:
#    pass
