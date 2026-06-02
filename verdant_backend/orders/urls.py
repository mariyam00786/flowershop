from django.urls import path
from .views import (
    CartDetailView,
    CartAddView,
    CartItemUpdateView,
    CartItemDeleteView,
    CartClearView,
    CartMergeView,
    ShippingAddressListCreateView,
    ShippingAddressUpdateDeleteView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderCancelView,
)

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('item/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('item/<int:pk>/remove/', CartItemDeleteView.as_view(), name='cart-item-remove'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
    path('merge/', CartMergeView.as_view(), name='cart-merge'),

    path('addresses/', ShippingAddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', ShippingAddressUpdateDeleteView.as_view(), name='address-update-delete'),

    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]
