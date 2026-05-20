from django.contrib import admin
from .models import Coupon, Order, OrderItem

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'max_uses', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_until')
    search_fields = ('code',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'payment_method', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'order_status', 'created_at')
    search_fields = ('id', 'user__username', 'gateway_order_id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)
    
    # Allow admin to manually update order status
    fields = ('user', 'address', 'total', 'coupon', 'discount_amount', 'payment_method', 'payment_status', 'order_status', 'gateway_order_id', 'created_at')
