from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from cart.models import Cart
from accounts.models import Address
from .models import Coupon, Order, OrderItem
from decimal import Decimal
from django.urls import reverse

@login_required
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.total_items == 0:
        messages.info(request, "Your cart is empty. Please add flowers before checkout.")
        return redirect('store:product_list')
        
    addresses = request.user.addresses.all()
    default_address = addresses.filter(is_default=True).first() or addresses.first()
    
    context = {
        'cart': cart,
        'addresses': addresses,
        'default_address': default_address,
    }
    return render(request, 'orders/checkout.html', context)

def validate_coupon_ajax(request):
    code = request.GET.get('code', '').strip().upper()
    if not code:
        return JsonResponse({'success': False, 'message': 'No coupon code provided.'})
        
    coupon = Coupon.objects.filter(code=code, is_active=True).first()
    if not coupon:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
        
    if not coupon.is_valid:
        return JsonResponse({'success': False, 'message': 'This coupon is expired or has reached its maximum uses.'})
        
    return JsonResponse({
        'success': True,
        'code': coupon.code,
        'discount_percent': coupon.discount_percent,
        'message': f"Coupon '{coupon.code}' applied! You save {coupon.discount_percent}%."
    })

@login_required
@require_POST
def place_order_ajax(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.total_items == 0:
        return JsonResponse({'success': False, 'message': 'Your cart is empty.'})
        
    address_id = request.POST.get('address_id')
    coupon_code = request.POST.get('coupon_code', '').strip().upper()
    payment_method = request.POST.get('payment_method')
    
    if not address_id:
        return JsonResponse({'success': False, 'message': 'Please select a delivery address.'})
        
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    
    if payment_method not in dict(Order.PAYMENT_METHODS):
        return JsonResponse({'success': False, 'message': 'Invalid payment method selected.'})
        
    # Calculate totals
    subtotal = cart.total_price
    discount = Decimal('0.00')
    coupon = None
    
    if coupon_code:
        coupon_obj = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon_obj and coupon_obj.is_valid:
            coupon = coupon_obj
            discount = subtotal * (Decimal(str(coupon.discount_percent)) / Decimal('100.00'))
            
    total = subtotal - discount
    if total < 0:
        total = Decimal('0.00')
        
    # Check inventory stock limits
    for item in cart.items.all():
        if item.product.stock < item.quantity:
            return JsonResponse({'success': False, 'message': f"Insufficient stock for '{item.product.name}'. Only {item.product.stock} left."})

    # Create Order
    order = Order.objects.create(
        user=request.user,
        address=address,
        total=total,
        coupon=coupon,
        discount_amount=discount,
        payment_method=payment_method,
        payment_status='UNPAID',
        order_status='Pending'
    )
    
    # Create OrderItems
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        
    # RAZORPAY GATEWAY PAYMENT
    if payment_method == 'RAZORPAY':
        return JsonResponse({
            'success': True,
            'payment_needed': True,
            'gateway': 'RAZORPAY',
            'order_id': order.id,
            'redirect_url': reverse('payments:razorpay_checkout', kwargs={'order_id': order.id})
        })

    return JsonResponse({'success': False, 'message': 'Unknown payment routing error.'})

@login_required
def confirmation_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def order_history_view(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = order.items.all().select_related('product')
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})
