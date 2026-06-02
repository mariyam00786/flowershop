from rest_framework import serializers
from .models import Cart, CartItem, ShippingAddress, Order, OrderItem
from products.serializers import PlantVariantSerializer
from products.models import PlantVariant, PotColor, Plant


class CartItemSerializer(serializers.ModelSerializer):
    variant = PlantVariantSerializer(read_only=True)
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    pot_color_name = serializers.CharField(source='pot_color.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'plant', 'plant_name', 'variant', 'pot_color', 'pot_color_name', 'quantity', 'line_total', 'primary_image']
        read_only_fields = ['id', 'line_total', 'plant_name', 'primary_image', 'pot_color_name']

    def get_primary_image(self, obj):
        return obj.plant.primary_image


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'session_key', 'user', 'created_at', 'items', 'subtotal']
        read_only_fields = ['id', 'session_key', 'user', 'created_at', 'items', 'subtotal']


class CartAddSerializer(serializers.Serializer):
    plant_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    pot_color_id = serializers.IntegerField(required=False, allow_null=True)
    qty = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        try:
            attrs['plant'] = Plant.objects.get(pk=attrs['plant_id'], is_active=True)
        except Plant.DoesNotExist:
            raise serializers.ValidationError({'plant_id': 'Plant not found'})
        try:
            attrs['variant'] = PlantVariant.objects.get(pk=attrs['variant_id'], plant=attrs['plant'])
        except PlantVariant.DoesNotExist:
            raise serializers.ValidationError({'variant_id': 'Variant not found'})
        if attrs.get('pot_color_id'):
            try:
                attrs['pot_color'] = PotColor.objects.get(pk=attrs['pot_color_id'])
            except PotColor.DoesNotExist:
                raise serializers.ValidationError({'pot_color_id': 'Pot color not found'})
        return attrs


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        read_only_fields = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'plant', 'plant_name', 'variant', 'pot_color', 'quantity', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(queryset=ShippingAddress.objects.all(), write_only=True, source='shipping_address')

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'shipping_address', 'shipping_address_id', 'status', 'subtotal', 'shipping_charge', 'total_amount', 'payment_method', 'notes', 'created_at', 'items']
        read_only_fields = ['id', 'order_number', 'user', 'status', 'subtotal', 'shipping_charge', 'total_amount', 'created_at', 'items']


class OrderCreateSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHODS)
    notes = serializers.CharField(required=False, allow_blank=True)
    shipping_option = serializers.ChoiceField(choices=[('standard', 'Standard'), ('express', 'Express')], default='standard')

    def validate_shipping_address_id(self, value):
        user = self.context['request'].user
        try:
            return ShippingAddress.objects.get(pk=value, user=user)
        except ShippingAddress.DoesNotExist:
            raise serializers.ValidationError('Shipping address not found.')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        cart = self.context['cart']
        if not cart.items.exists():
            raise serializers.ValidationError('Cart is empty.')
        shipping_charge = 49 if validated_data['shipping_option'] == 'standard' else 149
        subtotal = cart.subtotal
        total_amount = subtotal + shipping_charge
        order = Order.objects.create(
            user=user,
            shipping_address=validated_data['shipping_address_id'],
            subtotal=subtotal,
            shipping_charge=shipping_charge,
            total_amount=total_amount,
            payment_method=validated_data['payment_method'],
            notes=validated_data.get('notes', ''),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                plant=item.plant,
                variant=item.variant,
                pot_color=item.pot_color.name if item.pot_color else '',
                quantity=item.quantity,
                unit_price=item.variant.display_price,
            )
            item.variant.stock_quantity = max(item.variant.stock_quantity - item.quantity, 0)
            item.variant.save()
        cart.items.all().delete()
        return order
