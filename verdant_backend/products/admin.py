from django.contrib import admin
from .models import Category, Plant, PlantVariant, PlantImage, PotColor


class PlantVariantInline(admin.TabularInline):
    model = PlantVariant
    extra = 0


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'care_level', 'sunlight_requirement', 'is_active', 'created_at')
    list_filter = ('is_active', 'care_level', 'sunlight_requirement', 'is_pet_safe')
    search_fields = ('name', 'botanical_name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlantVariantInline, PlantImageInline]


@admin.register(PotColor)
class PotColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_color')
