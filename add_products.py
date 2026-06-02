#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antigravity_flowers.settings')
django.setup()

from store.models import Category, Product

# Create categories
categories = {
    'Luxury Bouquets': 'Premium curated bouquets perfect for special occasions and gifts',
    'Single Flowers': 'Exquisite individual stems for minimalist arrangements',
    'Flower Boxes': 'Beautiful arranged flowers in luxury gift boxes',
    'Gift Hampers': 'Complete luxury floral gift sets with premium add-ons'
}

created_cats = {}
for cat_name, cat_desc in categories.items():
    cat, created = Category.objects.get_or_create(name=cat_name)
    created_cats[cat_name] = cat
    if created:
        print(f"✓ Created category: {cat_name}")
    else:
        print(f"→ Category already exists: {cat_name}")

# Create products
products_data = [
    {
        'name': 'Tulip Bouquet',
        'category': 'Luxury Bouquets',
        'price': 220,
        'description': 'A premium bouquet of fresh, crisp white and soft pink tulips, perfectly wrapped in luxury textured tissue paper and tied with a silk ribbon.',
        'stock': 50,
        'is_featured': True
    },
    {
        'name': 'White Rose Bouquet',
        'category': 'Luxury Bouquets',
        'price': 350,
        'description': 'An exquisite, heavy bridal-style bouquet of premium white roses with dark green eucalyptus leaves, wrapped in elegant translucent vellum paper.',
        'stock': 40,
        'is_featured': True
    },
    {
        'name': 'Blue Iris Single',
        'category': 'Single Flowers',
        'price': 65,
        'description': 'A stunning, crisp, premium long-stemmed Royal Blue Iris flower with velvety texture and elegant side lighting.',
        'stock': 100,
        'is_featured': False
    },
    {
        'name': 'Red Gerbera Single',
        'category': 'Single Flowers',
        'price': 55,
        'description': 'A vibrant deep-red Gerbera daisy with a flawless petal arrangement and long clean green stem.',
        'stock': 100,
        'is_featured': False
    },
    {
        'name': 'Pink Carnation Single',
        'category': 'Single Flowers',
        'price': 49,
        'description': 'A fluffy light pink carnation blossom with delicate ruffled edges, perfect for intimate arrangements.',
        'stock': 120,
        'is_featured': False
    },
    {
        'name': 'Luxury Flower Box',
        'category': 'Flower Boxes',
        'price': 450,
        'description': 'A premium round suede gift box in dusty rose pink, overflowing with white roses and blush carnations.',
        'stock': 35,
        'is_featured': True
    },
    {
        'name': 'Anniversary Flower Hamper',
        'category': 'Gift Hampers',
        'price': 599,
        'description': 'An opulent luxury gift hamper featuring a massive arrangement of red roses, premium purple orchids, luxury room mist, and an elegant greeting card.',
        'stock': 20,
        'is_featured': True
    },
    {
        'name': 'Birthday Bouquet Box',
        'category': 'Gift Hampers',
        'price': 380,
        'description': 'A celebratory yet elegant luxury square white box filled with a vibrant arrangement of yellow sunflowers, pink tulips, and purple lavender.',
        'stock': 30,
        'is_featured': True
    }
]

for prod in products_data:
    category = created_cats[prod['category']]
    product, created = Product.objects.get_or_create(
        name=prod['name'],
        category=category,
        defaults={
            'description': prod['description'],
            'price': prod['price'],
            'stock': prod['stock'],
            'is_featured': prod['is_featured']
        }
    )
    if created:
        print(f"✓ Created product: {prod['name']} - AED {prod['price']}")
    else:
        print(f"→ Product already exists: {prod['name']}")

print("\n✓ All categories and products added successfully!")
