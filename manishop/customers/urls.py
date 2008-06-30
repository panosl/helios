from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'customers.views.customer'),
	(r'^register/$', 'customers.views.customer'),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', 'django.contrib.auth.views.logout'),
	(r'^reset-password/$', 'django.contrib.auth.views.password_reset'),
)
