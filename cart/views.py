from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product
from .models import Cart, CartItem

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

def _get_cart_json_data(cart):
    items_data = []
    for item in cart.items.all().select_related('product'):
        items_data.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_price': float(item.product.price),
            'product_image': item.product.primary_image,
            'product_slug': item.product.slug,
            'quantity': item.quantity,
            'subtotal': float(item.subtotal),
            'stock': item.product.stock,
        })
    
    # Dynamic lookup for upsell product IDs
    helium_balloon = Product.objects.filter(slug='helium-balloon').first()
    luxury_chocolates = Product.objects.filter(slug='luxury-chocolates').first()
    upsell_ids = {}
    if helium_balloon:
        upsell_ids['helium-balloon'] = helium_balloon.id
    if luxury_chocolates:
        upsell_ids['luxury-chocolates'] = luxury_chocolates.id
        
    return {
        'cart_total_items': cart.total_items,
        'cart_total_price': float(cart.total_price),
        'items': items_data,
        'upsell_ids': upsell_ids
    }

def cart_detail_view(request):
    cart = _get_or_create_cart(request)
    items = cart.items.all().select_related('product')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            **_get_cart_json_data(cart)
        })
        
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'items': items})

def cart_add_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_or_create_cart(request)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': "Invalid quantity selected."}, status=400)
            messages.error(request, "Invalid quantity selected.")
            return redirect('store:product_detail', slug=product.slug)
            
        # Inventory check
        if product.stock < quantity:
            msg = f"Sorry, only {product.stock} units are currently in stock for {product.name}."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
            return redirect('store:product_detail', slug=product.slug)
            
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            # Check if total exceeds stock
            if product.stock < (cart_item.quantity + quantity):
                msg = f"Cannot add. Combined cart quantity would exceed available stock."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': msg}, status=400)
                messages.error(request, msg)
                return redirect('store:product_detail', slug=product.slug)
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        success_msg = f"Added {quantity} x '{product.name}' to your cart!"
        messages.success(request, success_msg)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': success_msg,
                **_get_cart_json_data(cart)
            })
            
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart:cart_detail')

def cart_update_view(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        product = cart_item.product
        success_msg = ""
        error_msg = ""
        
        if action == 'increment':
            if product.stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
                success_msg = f"Increased quantity of {product.name}."
                messages.success(request, success_msg)
            else:
                error_msg = f"Cannot increase. Only {product.stock} items are in stock."
                messages.error(request, error_msg)
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                success_msg = f"Decreased quantity of {product.name}."
                messages.success(request, success_msg)
            else:
                cart_item.delete()
                success_msg = f"Removed {product.name} from your cart."
                messages.success(request, success_msg)
        elif action == 'set':
            try:
                qty = int(request.POST.get('quantity'))
                if qty <= 0:
                    cart_item.delete()
                    success_msg = f"Removed {product.name} from your cart."
                    messages.success(request, success_msg)
                elif product.stock >= qty:
                    cart_item.quantity = qty
                    cart_item.save()
                    success_msg = f"Updated quantity of {product.name} to {qty}."
                    messages.success(request, success_msg)
                else:
                    error_msg = f"Cannot update. Only {product.stock} items are in stock."
                    messages.error(request, error_msg)
            except (ValueError, TypeError):
                error_msg = "Invalid quantity value."
                messages.error(request, error_msg)
                
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if error_msg:
                return JsonResponse({'success': False, 'message': error_msg}, status=400)
            return JsonResponse({
                'success': True,
                'message': success_msg,
                **_get_cart_json_data(cart)
            })
            
    return redirect('cart:cart_detail')

def cart_remove_view(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    success_msg = f"Removed '{product_name}' from your cart."
    messages.success(request, success_msg)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': success_msg,
            **_get_cart_json_data(cart)
        })
        
    return redirect('cart:cart_detail')
