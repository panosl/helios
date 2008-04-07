from django.conf import settings


IS_MULTILINGUAL = getattr(settings, 'FAQ_IS_MULTILINGUAL', False)
