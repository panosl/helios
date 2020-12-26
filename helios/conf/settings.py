# -*- coding: utf-8 -*-
from django.conf import settings


DEBUG = getattr(settings, 'STORE_DEBUG', False)
PAGINATE_BY = getattr(settings, 'STORE_PAGINATE_BY', 50)
IS_MULTILINGUAL = getattr(settings, 'STORE_IS_MULTILINGUAL', False)
HAS_CURRENCIES = getattr(settings, 'STORE_HAS_CURRENCIES', False)
USE_PAYPAL = getattr(settings, 'STORE_USE_PAYPAL', False)
PRODUCT_MODEL = getattr(settings, 'STORE_PRODUCT_MODEL', 'helios.store.models.Product')
CART = getattr(settings, 'STORE_CART', 'helios.store.cart')
