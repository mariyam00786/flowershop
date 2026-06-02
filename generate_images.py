#!/usr/bin/env python
"""
Generate and download sample product/category images from Unsplash
based on Rose & Ivy collection prompts
"""

import os
import requests
from pathlib import Path

# Create media directories if they don't exist
MEDIA_ROOT = Path(__file__).parent / 'media'
CATEGORIES_DIR = MEDIA_ROOT / 'categories'
PRODUCTS_DIR = MEDIA_ROOT / 'products'

CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

# Direct image URLs for flower photos (from Pexels/Unsplash - stable URLs)
category_images = {
    'Luxury Bouquets': {
        'url': 'https://images.pexels.com/photos/50582/rose-flower-red-flowers-bloom-50582.jpeg',
        'filename': 'luxury-bouquets.jpg'
    },
    'Single Flowers': {
        'url': 'https://images.pexels.com/photos/36717/amazing-animal-beautiful-beautifull.jpg',
        'filename': 'single-flowers.jpg'
    },
    'Flower Boxes': {
        'url': 'https://images.pexels.com/photos/5632389/pexels-photo-5632389.jpeg',
        'filename': 'flower-boxes.jpg'
    },
    'Gift Hampers': {
        'url': 'https://images.pexels.com/photos/2835901/pexels-photo-2835901.jpeg',
        'filename': 'gift-hampers.jpg'
    }
}

# Direct image URLs for products
product_images = {
    'Tulip Bouquet': {
        'url': 'https://images.pexels.com/photos/842252/pexels-photo-842252.jpeg',
        'filename': 'tulip-bouquet.jpg'
    },
    'White Rose Bouquet': {
        'url': 'https://images.pexels.com/photos/50581/rose-white-flower-bloom-50581.jpeg',
        'filename': 'white-rose-bouquet.jpg'
    },
    'Blue Iris Single': {
        'url': 'https://images.pexels.com/photos/459335/pexels-photo-459335.jpeg',
        'filename': 'blue-iris-single.jpg'
    },
    'Red Gerbera Single': {
        'url': 'https://images.pexels.com/photos/380591/pexels-photo-380591.jpeg',
        'filename': 'red-gerbera-single.jpg'
    },
    'Pink Carnation Single': {
        'url': 'https://images.pexels.com/photos/167316/pexels-photo-167316.jpeg',
        'filename': 'pink-carnation-single.jpg'
    },
    'Luxury Flower Box': {
        'url': 'https://images.pexels.com/photos/5632382/pexels-photo-5632382.jpeg',
        'filename': 'luxury-flower-box.jpg'
    },
    'Anniversary Flower Hamper': {
        'url': 'https://images.pexels.com/photos/5632388/pexels-photo-5632388.jpeg',
        'filename': 'anniversary-hamper.jpg'
    },
    'Birthday Bouquet Box': {
        'url': 'https://images.pexels.com/photos/5632385/pexels-photo-5632385.jpeg',
        'filename': 'birthday-bouquet.jpg'
    }
}

def download_image(image_url, destination_path):
    """Download image from direct URL"""
    try:
        print(f"  Downloading from: {image_url[:60]}...")
        response = requests.get(image_url, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        # Save the image
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        
        file_size_kb = destination_path.stat().st_size / 1024
        print(f"  ✅ Saved: {destination_path.name} ({file_size_kb:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"  ⚠️ Warning: Could not download. Error: {str(e)[:50]}")
        print(f"     You can manually upload images via admin panel")
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
        download_image(image_info['url'], destination)
    
    # Download product images
    print("\n\n📁 DOWNLOADING PRODUCT IMAGES...")
    print("-" * 70)
    for product_name, image_info in product_images.items():
        print(f"\n🌸 {product_name}")
        destination = PRODUCTS_DIR / image_info['filename']
        download_image(image_info['url'], destination)
    
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
