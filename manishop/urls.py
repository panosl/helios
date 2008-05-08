'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^(?:en|el)/', include('manishop-urls'))
)
'''
import os
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.static import serve
from django.views.generic.simple import redirect_to
from store.views import orders_report


urlpatterns = patterns('',
	(r'^$', redirect_to, {'url': 'store'}),
	(r'^i18n/', include('django.conf.urls.i18n')),

	(r'^store/', include('store.urls')),
	(r'^customer/', include('customers.urls')),
	(r'^help/', include('faq.urls')),
	(r'^admin/store/order/report', orders_report),
	(r'^admin/', include('django.contrib.admin.urls')),

	#TODO should be removed when we move up from 0.96.1
	(r'^accounts/profile/$', redirect_to, {'url': '/store'}),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(os.path.abspath(os.path.curdir), 'static')}),
	)
