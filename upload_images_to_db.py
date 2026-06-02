#!/usr/bin/env python
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antigravity_flowers.settings')
django.setup()

from store.models import Category, Product
from django.core.files.base import ContentFile

# Define images to upload
categories_to_update = {
    'Single Flowers': 'media/categories/single-flowers.jpg',
    'Flower Boxes': 'media/categories/flower-boxes.jpg',
    'Gift Hampers': 'media/categories/gift-hampers.jpg',
}

products_to_update = {
    'Blue Iris Single': 'media/products/blue-iris-single.jpg',
    'Red Gerbera Single': 'media/products/red-gerbera-single.jpg',
    'Luxury Flower Box': 'media/products/luxury-flower-box.jpg',
    'Anniversary Flower Hamper': 'media/products/anniversary-hamper.jpg',
    'Birthday Bouquet Box': 'media/products/birthday-bouquet.jpg',
}

print("\n" + "="*70)
print("🌹 UPLOADING IMAGES TO DATABASE")
print("="*70)

# Upload category images
print("\n📁 UPDATING CATEGORIES...")
print("-" * 70)
for category_name, image_path in categories_to_update.items():
    try:
        if Path(image_path).exists():
            category = Category.objects.get(name=category_name)
            
            # Read the image file
            with open(image_path, 'rb') as f:
                file_content = ContentFile(f.read())
                filename = Path(image_path).name
                
                # Delete old image if it exists
                if category.image:
                    category.image.delete()
                
                # Upload new image
                category.image.save(filename, file_content, save=True)
            
            print(f"✅ {category_name}: Image uploaded ({Path(image_path).stat().st_size / 1024:.1f} KB)")
        else:
            print(f"⚠️ {category_name}: File not found at {image_path}")
    except Category.DoesNotExist:
        print(f"❌ {category_name}: Category not found in database")
    except Exception as e:
        print(f"❌ {category_name}: Error - {str(e)[:50]}")

# Upload product images
print("\n🌸 UPDATING PRODUCTS...")
print("-" * 70)
for product_name, image_path in products_to_update.items():
    try:
        if Path(image_path).exists():
            product = Product.objects.get(name=product_name)
            
            # Read the image file
            with open(image_path, 'rb') as f:
                file_content = ContentFile(f.read())
                filename = Path(image_path).name
                
                # Delete old image if it exists
                if product.image:
                    product.image.delete()
                
                # Upload new image
                product.image.save(filename, file_content, save=True)
            
            print(f"✅ {product_name}: Image uploaded ({Path(image_path).stat().st_size / 1024:.1f} KB)")
        else:
            print(f"⚠️ {product_name}: File not found at {image_path}")
    except Product.DoesNotExist:
        print(f"❌ {product_name}: Product not found in database")
    except Exception as e:
        print(f"❌ {product_name}: Error - {str(e)[:50]}")

print("\n" + "="*70)
print("✅ IMAGE UPLOAD TO DATABASE COMPLETE!")
print("="*70)
print("\n🌐 Check the website: http://127.0.0.1:8000/")
print("   Images should appear automatically on collections/products!\n")
