from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Address, Wallet, WalletTransaction
from orders.models import Order
from store.models import Wishlist
from decimal import Decimal
from django.urls import reverse
from django import forms

# Forms
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'street', 'city', 'state', 'pincode', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Trigger custom profile update if needed
            email = form.cleaned_data.get('email')
            user.email = email
            user.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome to Rose & Ivy, {user.username}! A startup bonus of AED 500.00 has been credited to your wallet.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Registration details were invalid. Please correct the errors.")
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('store:home')

@login_required
def profile_view(request):
    addresses = request.user.addresses.all()
    orders = request.user.orders.all()
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'addresses': addresses,
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def address_create_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Delivery address successfully added.")
            # Check if requested redirect parameter exists
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:profile')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add New Address'})

@login_required
def address_update_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery address successfully updated.")
            return redirect('accounts:profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})

@login_required
def address_delete_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, "Address successfully deleted.")
    return redirect('accounts:profile')

@login_required
def address_set_default_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, f"{address.full_name}'s address is now set as your default.")
    return redirect('accounts:profile')

@login_required
def wallet_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all().order_by('-created_at')
    return render(request, 'accounts/wallet.html', {'wallet': wallet, 'transactions': transactions})

@login_required
def wallet_add_funds(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount_dec = Decimal(amount)
            if amount_dec <= 0:
                raise ValueError("Amount must be greater than zero.")
            wallet = request.user.wallet
            wallet.credit(amount_dec, description="Self-deposited test credits")
            messages.success(request, f"Successfully topped up AED {amount_dec} test credits into your wallet!")
        except Exception as e:
            messages.error(request, f"Failed to add funds: {str(e)}")
    return redirect('accounts:wallet')
