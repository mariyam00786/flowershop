from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, ProductImage, Wishlist, Review

def home_view(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    categories = Category.objects.all()
    
    # Grab a few top review items or best sellers
    new_arrivals = Product.objects.all().order_by('-created_at')[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'store/home.html', context)

def product_list_view(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Filtering by category (slug)
    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
        
    # Filtering by Search Query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        
    # Filtering by Price Range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
            
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': query,
    }
    return render(request, 'store/product_list.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()
    reviews = product.reviews.all()
    
    # Related Products: in same category, exclude current
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    
    # Check if this item is in the logged-in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        
    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_toggle_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"Removed '{product.name}' from your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f"Added '{product.name}' to your wishlist!")
        
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('store:wishlist')

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        try:
            rating_val = int(rating)
            if rating_val < 1 or rating_val > 5:
                raise ValueError()
            
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(product=product, user=request.user).first()
            if existing_review:
                existing_review.rating = rating_val
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Your review has been updated.")
            else:
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating_val,
                    comment=comment
                )
                messages.success(request, "Thank you for reviewing this product!")
        except Exception:
            messages.error(request, "Failed to submit review. Please ensure you selected a valid star rating.")
            
    return redirect('store:product_detail', slug=product.slug)
