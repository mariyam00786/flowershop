import uuid
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, ShippingAddress, Order
from .serializers import (
    CartSerializer,
    CartAddSerializer,
    CartItemSerializer,
    ShippingAddressSerializer,
    OrderSerializer,
    OrderCreateSerializer,
)


def resolve_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, defaults={'session_key': ''})
        return cart

    session_key = request.headers.get('X-Session-Key') or request.query_params.get('session_key')
    if not session_key:
        session_key = uuid.uuid4().hex
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


class CartDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def get_object(self):
        return resolve_cart(self.request)

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        data = serializer.data
        if not request.user.is_authenticated:
            data['session_key'] = cart.session_key
        return Response(data)


class CartAddView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartAddSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = resolve_cart(request)
        payload = serializer.validated_data
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            plant=payload['plant'],
            variant=payload['variant'],
            pot_color=payload.get('pot_color'),
            defaults={'quantity': payload['qty']},
        )
        if not created:
            item.quantity += payload['qty']
            item.save()
        return Response({'detail': 'Item added to cart.', 'cart_id': cart.id, 'session_key': cart.session_key}, status=status.HTTP_200_OK)


class CartItemUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart=resolve_cart(self.request))

    def patch(self, request, *args, **kwargs):
        item = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is None or int(quantity) < 1:
            return Response({'detail': 'Quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = int(quantity)
        item.save()
        return Response(self.get_serializer(item).data)


class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CartItem.objects.filter(cart=resolve_cart(self.request))


class CartClearView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        cart = resolve_cart(request)
        cart.items.all().delete()
        return Response({'detail': 'Cart cleared.'}, status=status.HTTP_204_NO_CONTENT)


class CartMergeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        session_key = request.data.get('session_key')
        if not session_key:
            return Response({'detail': 'Session key is required to merge cart.'}, status=status.HTTP_400_BAD_REQUEST)
        guest_cart = get_object_or_404(Cart, session_key=session_key)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        for item in guest_cart.items.all():
            existing, created = CartItem.objects.get_or_create(
                cart=user_cart,
                plant=item.plant,
                variant=item.variant,
                pot_color=item.pot_color,
                defaults={'quantity': item.quantity},
            )
            if not created:
                existing.quantity += item.quantity
                existing.save()
        guest_cart.delete()
        return Response({'detail': 'Cart merged successfully.'}, status=status.HTTP_200_OK)


class ShippingAddressListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShippingAddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


class OrderCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        cart = resolve_cart(request)
        serializer = self.get_serializer(data=request.data, context={'request': request, 'cart': cart})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'order_number'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCancelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id, user=request.user)
        if order.status in ['shipped', 'delivered']:
            return Response({'detail': 'Cannot cancel an order that has already shipped.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        return Response({'detail': 'Order cancelled successfully.'}, status=status.HTTP_200_OK)
