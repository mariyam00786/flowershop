from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Stripe Card routes
    path('stripe/checkout/<int:order_id>/', views.stripe_checkout_view, name='stripe_checkout'),
    path('stripe/success/', views.stripe_success_view, name='stripe_success'),
    path('stripe/cancel/', views.stripe_cancel_view, name='stripe_cancel'),
    
    # Razorpay Indian routes
    path('razorpay/checkout/<int:order_id>/', views.razorpay_checkout_view, name='razorpay_checkout'),
    path('razorpay/verify/', views.razorpay_verify_view, name='razorpay_verify'),
]
