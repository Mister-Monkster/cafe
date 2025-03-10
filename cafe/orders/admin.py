from django.contrib import admin

from orders.models import OrderItem, Products, Orders


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_price')
    list_filter = ('status',)
    inlines = [OrderItemInline]


@admin.register(Products)
class ProdictsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
