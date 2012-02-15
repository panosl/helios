import os
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.static import serve
from django.views.generic.simple import redirect_to


urlpatterns = patterns('',
	(r'^$', redirect_to, {'url': 'store'}),
	(r'^store/', include('store.urls')),
	(r'^customer/', include('customers.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$',
		serve,
		{'document_root': os.path.join(os.path.abspath(os.path.curdir),
			'static')}),
	)
