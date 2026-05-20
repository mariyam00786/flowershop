from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/coupon/apply/', views.validate_coupon_ajax, name='apply_coupon'),
    path('checkout/place-order/', views.place_order_ajax, name='place_order'), # handles direct creation for COD / Wallet, or prepares order for Stripe / Razorpay!
    path('confirmation/<int:order_id>/', views.confirmation_view, name='confirmation'),
    path('history/', views.order_history_view, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
]
