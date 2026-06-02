from rest_framework import serializers
from .models import Review
from products.models import Plant
from orders.models import OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'plant', 'user', 'user_name', 'rating', 'title', 'body', 'is_verified_purchase', 'is_approved', 'created_at']
        read_only_fields = ['id', 'user', 'user_name', 'is_verified_purchase', 'is_approved', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['plant', 'rating', 'title', 'body']

    def validate_plant(self, value):
        if not value.is_active:
            raise serializers.ValidationError('Cannot review an inactive product.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        plant = validated_data['plant']
        verified = OrderItem.objects.filter(order__user=user, plant=plant, order__status__in=['confirmed', 'packed', 'shipped', 'delivered']).exists()
        review = Review.objects.create(
            user=user,
            is_verified_purchase=verified,
            is_approved=False,
            **validated_data,
        )
        return review
