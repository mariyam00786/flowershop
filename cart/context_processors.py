from .models import Cart

def cart_processor(request):
    cart_total_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_total_items = cart.total_items
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                cart_total_items = cart.total_items
    
    return {
        'cart_total_items': cart_total_items
    }
