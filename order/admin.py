from django.contrib import admin

from order.models import Order, OrderTour


class OrderTourInLine(admin.TabularInline):
    model = OrderTour


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderTourInLine]
    readonly_fields = ['total_price']


# admin.site.register(Order)
