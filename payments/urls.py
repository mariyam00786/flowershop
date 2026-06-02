from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Razorpay Indian routes
    path('razorpay/checkout/<int:order_id>/', views.razorpay_checkout_view, name='razorpay_checkout'),
    path('razorpay/verify/', views.razorpay_verify_view, name='razorpay_verify'),
]
