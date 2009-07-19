from django.contrib import admin
import multilingual
from helios.shipping.models import *


class ShipperAdmin(multilingual.ModelAdmin):
	prepopulated_fields = {'slug': ('name_en',)}

class ShippingRegionAdmin(multilingual.ModelAdmin):
	prepopulated_fields = {'slug': ('name_en', 'shipper')}
	list_display = [
		'name',
		'shipper',
		'desc',
	]

class ShippingMethodRegionsInline(admin.TabularInline):
	model = ShippingMethodRegions

class ShippingMethodAdmin(multilingual.ModelAdmin):
	inlines = [ShippingMethodRegionsInline]
	prepopulated_fields = {'slug': ('name_en', 'shipper')}
	list_display = [
		'name',
		'shipper',
	]

class ShippingMethodRegionsAdmin(admin.ModelAdmin):
	pass


admin.site.register(Shipper, ShipperAdmin)
admin.site.register(ShippingRegion, ShippingRegionAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(ShippingMethodRegions, ShippingMethodRegionsAdmin)
