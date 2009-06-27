from django.contrib import admin
import multilingual
from helios.orders.models import Order, OrderLine
from helios.store.forms import MyCategoryAdminForm
		

class OrderLineAdmin(admin.ModelAdmin):
	pass

class OrderLineInline(admin.TabularInline):
	model = OrderLine

class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderLineInline,]
	list_display = ['date_time_created', 'customer', 'status']
	list_filter = ('status',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
