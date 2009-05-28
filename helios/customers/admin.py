from django.contrib import admin
from helios.customers.models import CustomerProfile


class CustomerProfileAdmin(admin.ModelAdmin):
	pass

admin.site.register(CustomerProfile, CustomerProfileAdmin)
