from django.contrib import admin
from helios.orders.models import Order, OrderLine, OrderStatus
from helios.conf import settings
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


class OrderLineAdmin(admin.ModelAdmin):
    pass


class OrderLineInline(admin.TabularInline):
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time_created'
    inlines = [OrderLineInline]
    list_display = ['date_time_created', 'customer', 'status']
    list_filter = ('status',)


class OrderStatusAdmin(admin_info['class']):
    prepopulated_fields = {'slug': (''.join(['name', admin_info['suffix']]),)}


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
