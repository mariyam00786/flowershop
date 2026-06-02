from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from products.models import Plant
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class PlantReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        plant_slug = self.kwargs['plant_slug']
        plant = get_object_or_404(Plant, slug=plant_slug, is_active=True)
        return Review.objects.filter(plant=plant, is_approved=True)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
