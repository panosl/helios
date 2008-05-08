# -*- coding: utf-8 -*-
'''
    store.conf.settings
    ~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

from django.conf import settings


PAGINATE_BY = getattr(settings, 'STORE_PAGINATE_BY', 50)
IS_MULTILINGUAL = getattr(settings, 'STORE_IS_MULTILINGUAL', False)
