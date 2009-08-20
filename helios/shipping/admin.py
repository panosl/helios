from django.contrib import admin
from helios.shipping.models import *
if settings.IS_MULTILINGUAL:
	import multilingual
	admin_info = {
		'class': multilingual.ModelAdmin,
		'suffix': '_en'
	}
else:
	admin_info = {
		'class': admin.ModelAdmin,
		'suffix': ''
	}


class ShipperAdmin(admin_info['class']):
	prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}

class ShippingRegionAdmin(admin_info['class']):
	prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}
	list_display = [
		'name',
		'shipper',
		'desc',
	]
	filter_horizontal = ('countries',)

class ShippingMethodRegionsInline(admin.TabularInline):
	model = ShippingMethodRegions

class ShippingMethodAdmin(admin_info['class']):
	inlines = [ShippingMethodRegionsInline]
	prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}
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
