from django.contrib import admin
from multilingual.translation import TranslationModelAdmin
from helios.store.models import Currency, Category, Product, ProductImage, Order, OrderLine
from helios.store.conf import settings


class CurrencyAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'symbol', 'factor')
	list_display_links = ('name',)

class CategoryAdmin(admin.ModelAdmin):
	class Translation(TranslationModelAdmin):
		ordering= ('name', )
		#prepopulated_fields = {'slug': ('name',)}

	list_display = ('name', 'desc', 'parent')
	#prepopulated_fields = {'slug': (get_name(),)}
	#prepopulated_fields = {'slug': ('categorytranslation.0.name',)}

	#prepopulated_fields = {'slug': ('name_en',)}
	#if settings.IS_MULTILINGUAL:
	#	#prepopulated_fields = {'slug': (Product.translations.get(pk=1).name,)}
	#	prepopulated_fields = {'slug': ('category_translation.0.name',)}

class ProductImageInline(admin.TabularInline):
	model = ProductImage

#class ProductAdmin(admin.ModelAdmin):
	#inlines = [ProductImageInline,]
	#list_display = ('name', 'price', 'stock')
	#list_filter = ('category',)
	#prepopulated_fields = {'slug': ('name',)}
	#search_fields = ['slug', 'name']
class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImageInline,]
	list_filter = ('category',)
	list_display = ('name', 'price', 'stock')
	class Translation(TranslationModelAdmin):
		list_display = ('name', 'price', 'stock')

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
