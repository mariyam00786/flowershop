from django.contrib import admin
from .models import WishlistItem


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'added_at')
    search_fields = ('user__email', 'plant__name')
    list_filter = ('added_at',)
