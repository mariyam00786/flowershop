from django.urls import path
from .views import PlantReviewListView, ReviewCreateView

urlpatterns = [
    path('<slug:plant_slug>/', PlantReviewListView.as_view(), name='review-list'),
    path('create/', ReviewCreateView.as_view(), name='review-create'),
]
