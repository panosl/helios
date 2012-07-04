# -*- coding: utf-8 -*-
from django.contrib import admin
from helios.store.models import *
from helios.store.forms import MyCategoryAdminForm
from helios.conf import settings
if settings.IS_MULTILINGUAL:
    import multilingual
    admin_info = {
        'class': multilingual.ModelAdmin,
        'suffix': '_en'
    }
else:
    admin_info = {
        'class': admin.ModelAdmin,
        'suffix': ''
    }


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['picture', 'product']


class CategoryAdmin(admin_info['class']):
    form = MyCategoryAdminForm
    list_display = ('name', 'desc', 'parent')
    prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}


def set_category(modeladmin, request, queryset):
    categories = Category.objects.all()
    queryset.update(category)


class ProductAdmin(admin_info['class']):
    inlines = [ProductImageInline]
    list_display = ('name', 'base_price', 'price', 'stock', 'last_modified', 'category',)
    list_filter = ('category', 'is_active', 'is_featured',)
    prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}
    search_fields = ['name']


class TaxAdmin(admin_info['class']):
    list_display = ('name', 'rate', 'factor',)
    prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Tax, TaxAdmin)
