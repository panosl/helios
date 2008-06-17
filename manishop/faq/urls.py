# Hellios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2007 Panos Laganakos <panos.laganakos@gmail.com>

from django.conf.urls.defaults import *
from faq.models import FAQ


faq_dict = {
	'queryset': FAQ.objects.all(),
	'template_object_name': 'faq',
	'allow_empty': True,
}

urlpatterns = patterns('django.views.generic.list_detail',
	(r'^$', 'object_list', faq_dict),
)
