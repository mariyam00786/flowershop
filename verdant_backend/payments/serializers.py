from rest_framework import serializers
from .models import Payment


class RazorpayOrderCreateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)


class PaymentVerifySerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'amount', 'currency', 'status', 'payment_method', 'created_at']
