import hmac
import hashlib
import json
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from .models import Payment
from .serializers import RazorpayOrderCreateSerializer, PaymentVerifySerializer, PaymentSerializer


class RazorpayOrderCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RazorpayOrderCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.filter(id=serializer.validated_data['order_id'], user=request.user).first()
        if not order:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        if order.status != 'pending':
            return Response({'detail': 'Order is not eligible for payment.'}, status=status.HTTP_400_BAD_REQUEST)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            'amount': int(order.total_amount * 100),
            'currency': 'INR',
            'receipt': order.order_number,
            'payment_capture': 1,
        })
        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order['id'],
            amount=order.total_amount,
            currency='INR',
            status='pending',
            payment_method='razorpay',
        )
        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': int(order.total_amount * 100),
            'currency': 'INR',
            'payment_id': payment.id,
        })


class PaymentVerifyView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        payload = f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}"
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_signature, data['razorpay_signature']):
            return Response({'detail': 'Signature verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.filter(razorpay_order_id=data['razorpay_order_id']).order_by('-created_at').first()
        if not payment:
            return Response({'detail': 'Payment record not found.'}, status=status.HTTP_404_NOT_FOUND)
        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.razorpay_signature = data['razorpay_signature']
        payment.status = 'completed'
        payment.save()
        order = payment.order
        order.status = 'confirmed'
        order.save()
        return Response({'detail': 'Payment verified successfully.', 'order_number': order.order_number}, status=status.HTTP_200_OK)


@csrf_exempt
def razorpay_webhook_view(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    webhook_body = request.body.decode('utf-8')
    expected_signature = request.headers.get('X-Razorpay-Signature', '')
    secret = settings.RAZORPAY_KEY_SECRET
    generated_signature = hmac.new(secret.encode(), webhook_body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(generated_signature, expected_signature):
        return HttpResponse(status=400)

    event = request.headers.get('X-Razorpay-Event', '')
    payload = json.loads(webhook_body)
    razorpay_order_id = payload.get('payload', {}).get('order', {}).get('entity', {}).get('id')
    payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id).order_by('-created_at').first()
    if not payment:
        return HttpResponse(status=404)

    if event == 'payment.captured':
        payment.status = 'completed'
        payment.razorpay_payment_id = payload['payload']['payment']['entity']['id']
        payment.save()
        order = payment.order
        order.status = 'confirmed'
        order.save()
    elif event == 'payment.failed':
        payment.status = 'failed'
        payment.save()
    return HttpResponse(status=200)


class PaymentStatusView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    lookup_field = 'order_id'

    def get_object(self):
        return get_object_or_404(Payment, order_id=self.kwargs['order_id'])
