from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import WishlistItem
from .serializers import WishlistItemSerializer, WishlistAddSerializer


class WishlistListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


class WishlistAddView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistAddSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plant = serializer.validated_data['plant_id']
        item, created = WishlistItem.objects.get_or_create(user=request.user, plant=plant)
        if not created:
            return Response({'detail': 'Plant already in wishlist.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Plant added to wishlist.'}, status=status.HTTP_201_CREATED)


class WishlistRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WishlistItem.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user, pk=self.kwargs['pk']).first()

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        if not item:
            return Response({'detail': 'Wishlist item not found.'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({'detail': 'Removed from wishlist.'}, status=status.HTTP_204_NO_CONTENT)
