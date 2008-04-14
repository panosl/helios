#from django.conf.urls.defaults import *

#urlpatterns = patterns('',
#   (r'^(?:en|el)/', include('manishop-urls'))
#)
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/panosl/web-projects/manishop.gr/manishop/manigifts/static'}),
    (r'^$', redirect_to, {'url': 'store'}),
    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^store/', include('manigifts.store.urls')),
    (r'customer/', include('customers.urls')),
    (r'^help/', include('manigifts.faq.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^accounts/profile/$', redirect_to, {'url': '/store'}),
)
