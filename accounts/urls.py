from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/', views.profile_view, name='profile'),
    
    path('address/add/', views.address_create_view, name='address_add'),
    path('address/<int:pk>/edit/', views.address_update_view, name='address_edit'),
    path('address/<int:pk>/delete/', views.address_delete_view, name='address_delete'),
    path('address/<int:pk>/default/', views.address_set_default_view, name='address_default'),
    
    path('wallet/', views.wallet_view, name='wallet'),
    path('wallet/add-funds/', views.wallet_add_funds, name='wallet_add_funds'),
]
