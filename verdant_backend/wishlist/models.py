from django.db import models
from django.conf import settings
from products.models import Plant


class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist_items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='wishlist_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'plant')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email} – {self.plant.name}"
