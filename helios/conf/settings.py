# -*- coding: utf-8 -*-
from django.conf import settings


PAGINATE_BY = getattr(settings, 'STORE_PAGINATE_BY', 50)
IS_MULTILINGUAL = getattr(settings, 'STORE_IS_MULTILINGUAL', False)
USE_SORL = getattr(settings, 'STORE_USE_SORL', False)
USE_PAYPAL = getattr(settings, 'STORE_USE_PAYPAL', False)
