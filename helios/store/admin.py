from django.contrib import admin
#from multilingual.translation import TranslationModelAdmin
import multilingual
from helios.store.models import Currency, Category, Product, ProductImage, Order, OrderLine
from helios.store.conf import settings


class CurrencyAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'symbol', 'factor')
	list_display_links = ('name',)

class CategoryAdmin(multilingual.ModelAdmin):
	list_display = ('name', 'desc', 'parent')
	prepopulated_fields = {'slug': ('name_en',)}

class ProductImageInline(admin.TabularInline):
	model = ProductImage

class ProductAdmin(multilingual.ModelAdmin):
	inlines = [ProductImageInline,]
	list_filter = ('category',)
	list_display = ('name', 'price', 'stock')
	prepopulated_fields = {'slug': ('name_en',)}

class ProductImageAdmin(admin.ModelAdmin):
	list_display = ['picture', 'product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['date_time_created', 'customer', 'status']
	list_filter = ('status',)

class OrderLineAdmin(admin.ModelAdmin):
	pass

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
