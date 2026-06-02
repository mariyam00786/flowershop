from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user', 'rating', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'is_verified_purchase', 'rating')
    search_fields = ('plant__name', 'user__email', 'title', 'body')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'
