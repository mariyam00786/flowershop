from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from accounts.models import Address
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Percentage discount (e.g. 10 for 10%)")
    max_uses = models.PositiveIntegerField(default=100)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @property
    def is_valid(self):
        now = timezone.now()
        used_count = Order.objects.filter(coupon=self, payment_status='PAID').count()
        return self.is_active and now < self.valid_until and used_count < self.max_uses

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"

class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    
    PAYMENT_STATUS = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    PAYMENT_METHODS = (
        ('RAZORPAY', 'UPI/Net Banking (Razorpay)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='UNPAID')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    
    # Store dynamic metadata for gateway payments if needed (e.g. Stripe checkout session ID or Razorpay order ID)
    gateway_order_id = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price locked at purchase time

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Item {self.product.name} (x{self.quantity}) in Order #{self.order.id}"
