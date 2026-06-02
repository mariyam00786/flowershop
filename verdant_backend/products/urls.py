from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='product-categories'),
    path('', ProductListView.as_view(), name='product-list'),
    path('featured/', ProductListView.as_view(list_type='featured'), name='product-featured'),
    path('new-arrivals/', ProductListView.as_view(list_type='new-arrivals'), name='product-new-arrivals'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]
