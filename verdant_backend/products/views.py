from datetime import timedelta
from django.db.models import Q, F, Min, Avg
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Category, Plant
from .serializers import CategorySerializer, PlantListSerializer, PlantDetailSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class = PlantListSerializer
    permission_classes = [AllowAny]
    list_type = None

    def get_queryset(self):
        queryset = Plant.objects.filter(is_active=True)
        if getattr(self, 'list_type', None) == 'featured':
            queryset = queryset.filter(is_active=True, variants__stock_quantity__gt=0).distinct().order_by('-created_at')
        elif getattr(self, 'list_type', None) == 'new-arrivals':
            queryset = queryset.filter(created_at__gte=timezone.now() - timedelta(days=30))

        category = self.request.query_params.get('category')
        care_level = self.request.query_params.get('care_level')
        sunlight = self.request.query_params.get('sunlight')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        pet_safe = self.request.query_params.get('pet_safe')
        search = self.request.query_params.get('search')
        is_sale = self.request.query_params.get('is_sale')
        ordering = self.request.query_params.get('ordering')

        if category:
            queryset = queryset.filter(category__slug=category)
        if care_level:
            queryset = queryset.filter(care_level=care_level)
        if sunlight:
            queryset = queryset.filter(sunlight_requirement=sunlight)
        if pet_safe in ['true', 'True', '1']:
            queryset = queryset.filter(is_pet_safe=True)
        if is_sale in ['true', 'True', '1']:
            queryset = queryset.filter(variants__sale_price__isnull=False).distinct()
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(botanical_name__icontains=search) | Q(description__icontains=search))
        if min_price:
            queryset = queryset.filter(variants__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(variants__price__lte=max_price)

        queryset = queryset.annotate(
            min_variant_price=Min('variants__price'),
            average_rating=Avg('reviews__rating'),
        ).distinct()

        if ordering == 'price':
            queryset = queryset.order_by('min_variant_price')
        elif ordering == '-price':
            queryset = queryset.order_by('-min_variant_price')
        elif ordering == 'newest':
            queryset = queryset.order_by('-created_at')
        elif ordering == 'rating':
            queryset = queryset.order_by('-average_rating')

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Plant.objects.filter(is_active=True)
    serializer_class = PlantDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
