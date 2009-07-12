from django.contrib import admin
import multilingual
from helios.store.models import *
from helios.store.forms import MyCategoryAdminForm
		

class CategoryAdmin(multilingual.ModelAdmin):
	form = MyCategoryAdminForm
	list_display = ('name', 'desc', 'parent')
	prepopulated_fields = {'slug': ('name_en',)}

class ProductImageInline(admin.TabularInline):
	model = ProductImage

class ProductAdmin(multilingual.ModelAdmin):
	inlines = [ProductImageInline,]
	list_filter = ('category', 'is_active', 'is_featured',)
	list_display = ('name', 'price', 'stock', 'last_modified', 'date_added',)
	prepopulated_fields = {'slug': ('name_en',)}

class ProductImageAdmin(multilingual.ModelAdmin):
	list_display = ['picture', 'product']

class TaxAdmin(multilingual.ModelAdmin):
	prepopulated_fields = {'slug': ('name_en',)}

class OrderLineAdmin(admin.ModelAdmin):
	pass

class OrderLineInline(admin.TabularInline):
	model = OrderLine

class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderLineInline,]
	list_display = ['date_time_created', 'customer', 'status']
	list_filter = ('status',)

class ShippingMethodAdmin(multilingual.ModelAdmin):
	prepopulated_fields = {'slug': ('name_en',)}

class PaymentOptionAdmin(multilingual.ModelAdmin):
	prepopulated_fields = {'slug': ('name_en',)}
	

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(PaymentOption, PaymentOptionAdmin)
