from django.contrib import admin
from .models import Cart, CartItem, ShippingAddress, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('plant', 'variant', 'pot_color', 'quantity', 'line_total')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at')
    search_fields = ('user__email', 'session_key')
    inlines = [CartItemInline]


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'state', 'is_default')
    list_filter = ('state', 'is_default')
    search_fields = ('user__email', 'full_name', 'city', 'pincode')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('plant', 'variant', 'pot_color', 'quantity', 'unit_price', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('subtotal', 'shipping_charge', 'total_amount', 'created_at')
    inlines = [OrderItemInline]

    actions = ['mark_as_shipped', 'mark_as_delivered', 'export_orders_csv']

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Mark selected orders as shipped'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'

    def export_orders_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=verdant_orders.csv'
        writer = csv.writer(response)
        writer.writerow(['Order Number', 'Email', 'Status', 'Total', 'Created'])
        for order in queryset:
            writer.writerow([order.order_number, order.user.email, order.status, order.total_amount, order.created_at])
        return response
    export_orders_csv.short_description = 'Export selected orders to CSV'
