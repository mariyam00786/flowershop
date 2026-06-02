from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'amount', 'currency', 'payment_method', 'created_at')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('order__order_number', 'razorpay_order_id', 'razorpay_payment_id')
    list_filter = ('status', 'payment_method', 'currency')
