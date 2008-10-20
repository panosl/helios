from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'helios.customers.views.customer'),
	(r'^register/$', 'helios.customers.views.customer'),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', 'django.contrib.auth.views.logout'),
	(r'^reset-password/$', 'django.contrib.auth.views.password_reset'),
)
