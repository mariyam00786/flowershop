from rest_framework import serializers
from .models import WishlistItem
from products.serializers import PlantListSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    plant = PlantListSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'plant', 'added_at']


class WishlistAddSerializer(serializers.Serializer):
    plant_id = serializers.IntegerField()

    def validate_plant_id(self, value):
        from products.models import Plant
        try:
            return Plant.objects.get(pk=value, is_active=True)
        except Plant.DoesNotExist:
            raise serializers.ValidationError('Plant not found.')
