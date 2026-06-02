#!/usr/bin/env python
"""
Generate and download sample product/category images from Unsplash
based on Rose & Ivy collection prompts
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlencode

# Create media directories if they don't exist
MEDIA_ROOT = Path(__file__).parent / 'media'
CATEGORIES_DIR = MEDIA_ROOT / 'categories'
PRODUCTS_DIR = MEDIA_ROOT / 'products'

CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

# Unsplash API (free, no auth required for basic searches)
UNSPLASH_BASE = "https://source.unsplash.com/1200x800"

# Image search queries for categories
category_images = {
    'Luxury Bouquets': {
        'query': 'luxury premium roses pink peonies flowers bouquet',
        'filename': 'luxury-bouquets.jpg'
    },
    'Single Flowers': {
        'query': 'single flower iris blue macro close-up petal',
        'filename': 'single-flowers.jpg'
    },
    'Flower Boxes': {
        'query': 'luxury flower box arrangement roses emerald green',
        'filename': 'flower-boxes.jpg'
    },
    'Gift Hampers': {
        'query': 'luxury gift hamper flowers tulips lavender basket',
        'filename': 'gift-hampers.jpg'
    }
}

# Image search queries for products
product_images = {
    'Tulip Bouquet': {
        'query': 'white pink tulips bouquet fresh flowers',
        'filename': 'tulip-bouquet.jpg'
    },
    'White Rose Bouquet': {
        'query': 'white roses bouquet bridal premium luxury',
        'filename': 'white-rose-bouquet.jpg'
    },
    'Blue Iris Single': {
        'query': 'blue iris flower single stem macro photography',
        'filename': 'blue-iris-single.jpg'
    },
    'Red Gerbera Single': {
        'query': 'red gerbera daisy flower single stem macro',
        'filename': 'red-gerbera-single.jpg'
    },
    'Pink Carnation Single': {
        'query': 'pink carnation flower single stem ruffled petals',
        'filename': 'pink-carnation-single.jpg'
    },
    'Luxury Flower Box': {
        'query': 'luxury flower box roses pink white arrangement gift',
        'filename': 'luxury-flower-box.jpg'
    },
    'Anniversary Flower Hamper': {
        'query': 'luxury anniversary gift hamper red roses orchids',
        'filename': 'anniversary-hamper.jpg'
    },
    'Birthday Bouquet Box': {
        'query': 'colorful birthday flower bouquet celebration yellow pink purple',
        'filename': 'birthday-bouquet.jpg'
    }
}

def download_image(search_query, destination_path, width=1200, height=800):
    """Download image from Unsplash based on search query"""
    try:
        # Build Unsplash URL with search query
        url = f"{UNSPLASH_BASE}?{urlencode({'q': search_query})}"
        
        print(f"  Downloading from: {url}")
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        # Save the image
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        
        file_size_kb = destination_path.stat().st_size / 1024
        print(f"  ✅ Saved: {destination_path.name} ({file_size_kb:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error downloading: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🌹 ROSE & IVY - IMAGE GENERATION")
    print("="*70)
    
    # Download category images
    print("\n📁 DOWNLOADING CATEGORY IMAGES...")
    print("-" * 70)
    for category_name, image_info in category_images.items():
        print(f"\n📸 {category_name}")
        destination = CATEGORIES_DIR / image_info['filename']
        download_image(image_info['query'], destination)
    
    # Download product images
    print("\n\n📁 DOWNLOADING PRODUCT IMAGES...")
    print("-" * 70)
    for product_name, image_info in product_images.items():
        print(f"\n🌸 {product_name}")
        destination = PRODUCTS_DIR / image_info['filename']
        download_image(image_info['query'], destination)
    
    # Summary
    print("\n" + "="*70)
    print("✅ IMAGE DOWNLOAD COMPLETE!")
    print("="*70)
    
    category_count = len([f for f in CATEGORIES_DIR.glob('*.jpg')])
    product_count = len([f for f in PRODUCTS_DIR.glob('*.jpg')])
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Categories: {category_count}/{len(category_images)} images downloaded")
    print(f"   ✅ Products: {product_count}/{len(product_images)} images downloaded")
    
    print(f"\n📁 Image Locations:")
    print(f"   Categories: {CATEGORIES_DIR}")
    print(f"   Products: {PRODUCTS_DIR}")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Go to Django Admin: http://127.0.0.1:8000/admin/")
    print(f"   2. Upload images to each category/product")
    print(f"   3. Images will appear instantly on the website!")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()
