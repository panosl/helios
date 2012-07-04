# -*- coding: utf-8 -*-
from django.contrib import admin
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


class PaymentOptionAdmin(admin_info['class']):
    prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}


admin.site.register(PaymentOption, PaymentOptionAdmin)
