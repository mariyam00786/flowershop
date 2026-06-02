from rest_framework import serializers
from .models import Category, Plant, PlantVariant, PlantImage, PotColor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']


class PlantVariantSerializer(serializers.ModelSerializer):
    display_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = PlantVariant
        fields = ['id', 'size', 'price', 'sale_price', 'display_price', 'stock_quantity', 'sku']


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['id', 'image', 'is_primary', 'alt_text']


class PotColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotColor
        fields = ['id', 'name', 'hex_color', 'image']


class PlantListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.CharField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Plant
        fields = ['id', 'name', 'botanical_name', 'slug', 'category', 'primary_image', 'min_price', 'max_price', 'average_rating', 'review_count', 'care_level', 'is_pet_safe', 'is_air_purifying', 'created_at']


class PlantDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = PlantVariantSerializer(many=True, read_only=True)
    images = PlantImageSerializer(many=True, read_only=True)
    pot_colors = PotColorSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plant
        fields = [
            'id', 'name', 'botanical_name', 'slug', 'category', 'description', 'care_instructions',
            'sunlight_requirement', 'watering_frequency', 'temperature_range', 'humidity_level',
            'care_level', 'is_pet_safe', 'is_air_purifying', 'is_active', 'created_at',
            'variants', 'images', 'pot_colors', 'average_rating', 'review_count'
        ]
