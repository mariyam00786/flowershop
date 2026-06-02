from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = CloudinaryField('category_image', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plant(models.Model):
    SUNLIGHT_CHOICES = [
        ('low', 'Low'),
        ('indirect', 'Indirect'),
        ('bright', 'Bright'),
        ('direct', 'Direct'),
    ]

    CARE_LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('expert', 'Expert'),
    ]

    name = models.CharField(max_length=220)
    botanical_name = models.CharField(max_length=220, blank=True)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plants')
    description = models.TextField()
    care_instructions = models.TextField(blank=True)
    sunlight_requirement = models.CharField(max_length=20, choices=SUNLIGHT_CHOICES)
    watering_frequency = models.CharField(max_length=100)
    temperature_range = models.CharField(max_length=100)
    humidity_level = models.CharField(max_length=100)
    care_level = models.CharField(max_length=20, choices=CARE_LEVEL_CHOICES)
    is_pet_safe = models.BooleanField(default=False)
    is_air_purifying = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url
        first = self.images.first()
        return first.image.url if first else ''

    @property
    def min_price(self):
        variant = self.variants.order_by('price').first()
        return variant.price if variant else None

    @property
    def max_price(self):
        variant = self.variants.order_by('-price').first()
        return variant.price if variant else None

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def average_rating(self):
        ratings = self.reviews.filter(is_approved=True).values_list('rating', flat=True)
        return round(sum(ratings) / len(ratings), 1) if ratings else 0.0


class PlantVariant(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('xl', 'XL'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ('plant', 'size')

    def __str__(self):
        return f"{self.plant.name} - {self.size.title()}"

    @property
    def display_price(self):
        return self.sale_price if self.sale_price else self.price


class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('plant_image')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=180, blank=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            self.plant.images.filter(is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.plant.name}"


class PotColor(models.Model):
    name = models.CharField(max_length=80)
    hex_color = models.CharField(max_length=7)
    image = CloudinaryField('pot_color_image', blank=True, null=True)

    def __str__(self):
        return self.name
