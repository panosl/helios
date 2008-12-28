from django.contrib import admin
from helios.location.models import Country


class CountryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Country, CountryAdmin)
