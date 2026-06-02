from django.urls import path
from .views import (
    RazorpayOrderCreateView,
    PaymentVerifyView,
    razorpay_webhook_view,
    PaymentStatusView,
)

urlpatterns = [
    path('create-order/', RazorpayOrderCreateView.as_view(), name='payments-create-order'),
    path('verify/', PaymentVerifyView.as_view(), name='payments-verify'),
    path('webhook/', razorpay_webhook_view, name='payments-webhook'),
    path('<int:order_id>/', PaymentStatusView.as_view(), name='payments-status'),
]
