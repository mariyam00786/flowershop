from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with 18 requested premium flower and add-on products with real Unsplash photo URLs and AED pricing.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Preparing to seed premium flower products in AED...')

        # 1. Ensure Categories exist
        bouquets, _ = Category.objects.get_or_create(
            name='Bouquets', 
            slug='bouquets'
        )
        single_flowers, _ = Category.objects.get_or_create(
            name='Single Flowers', 
            slug='single-flowers'
        )
        plants, _ = Category.objects.get_or_create(
            name='Plants', 
            slug='plants'
        )
        gifts, _ = Category.objects.get_or_create(
            name='Gifts', 
            slug='gifts'
        )

        self.stdout.write('Clearing old products to ensure clean seed state...')
        Product.objects.all().delete()

        # 2. Product definitions
        products_data = [
            # BOUQUETS
            {
                'category': bouquets,
                'name': 'Red Rose Bouquet',
                'slug': 'red-rose-bouquet',
                'description': 'A stunning and classic arrangement of fresh premium crimson red roses, elegantly styled with baby\'s breath and silver dollar eucalyptus. The ultimate expression of love.',
                'price': Decimal('294.00'),
                'stock': 15,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=600'
            },
            {
                'category': bouquets,
                'name': 'Sunflower Bouquet',
                'slug': 'sunflower-bouquet',
                'description': 'Bring the radiant sunshine indoors with our cheerful bouquet of vibrant golden sunflowers, seasonal fillers, and rich wild foliage tied with a sage green bow.',
                'price': Decimal('189.00'),
                'stock': 20,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1504185945330-7a3ca1380535?w=600'
            },
            {
                'category': bouquets,
                'name': 'Mixed Wildflower Bouquet',
                'slug': 'mixed-wildflower-bouquet',
                'description': 'A charming and rustic hand-tied bouquet featuring a delightful blend of colorful seasonal wildflowers, soft lavender, and fresh eucalyptus greens.',
                'price': Decimal('245.00'),
                'stock': 12,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1490750967868-88df5691cc03?w=600'
            },
            {
                'category': bouquets,
                'name': 'Pink Peony Bouquet',
                'slug': 'pink-peony-bouquet',
                'description': 'A luxurious and soft arrangement of pillowy, fresh pink peonies, beautifully styled in our signature wrapping paper. Perfect for high-end gifting.',
                'price': Decimal('399.00'),
                'stock': 8,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1589994160839-163cd867cfe8?w=600'
            },
            
            # SINGLE FLOWERS
            {
                'category': single_flowers,
                'name': 'White Lily',
                'slug': 'white-lily',
                'description': 'A pristine, elegant single stem of majestic white lily showcasing large fragrant blooms. Symbolizes purity, elegance, and peace.',
                'price': Decimal('45.00'),
                'stock': 25,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1559563362-c667ba5f5480?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Pink Tulip',
                'slug': 'pink-tulip',
                'description': 'A beautifully crisp single stem of premium Dutch pink tulip. Graceful and simple, it brings a fresh pop of color to any room.',
                'price': Decimal('59.00'),
                'stock': 30,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1561328399-f94d2ce78679?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Blue Iris',
                'slug': 'blue-iris',
                'description': 'An exotic single stem of deep blue iris featuring striking purple-blue petals highlighted with bright golden-yellow markings.',
                'price': Decimal('69.00'),
                'stock': 15,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Yellow Marigold',
                'slug': 'yellow-marigold',
                'description': 'A vibrant single stem of bright yellow marigold, symbolizing passion, warmth, and creativity. Popular for festive decor and daily freshness.',
                'price': Decimal('39.00'),
                'stock': 30,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1598880940080-ff9a29891b85?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Red Gerbera Daisy',
                'slug': 'red-gerbera-daisy',
                'description': 'A cheerful, large-flowered single stem of bright red Gerbera daisy, guaranteed to uplift spirits with its bold color and classic form.',
                'price': Decimal('49.00'),
                'stock': 20,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Purple Lavender',
                'slug': 'purple-lavender',
                'description': 'A fragrant bundle of dried premium French purple lavender stems, popular for its soothing aromatherapy benefits and rustic visual charm.',
                'price': Decimal('79.00'),
                'stock': 28,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1611909023032-2d6b3134ecba?w=600'
            },
            
            # PLANTS
            {
                'category': plants,
                'name': 'Peace Lily Plant',
                'slug': 'peace-lily-plant',
                'description': 'An elegant and robust Peace Lily plant with lush dark green foliage and beautiful white flowers. Renowned for its superb air-purifying capabilities.',
                'price': Decimal('129.00'),
                'stock': 18,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1597055181449-b977fc38f91b?w=600'
            },
            {
                'category': plants,
                'name': 'Orchid Plant',
                'slug': 'orchid-plant',
                'description': 'A delicate and majestic potted Phalaenopsis orchid plant with multiple purple blooms. Comes in a sage green ceramic planter.',
                'price': Decimal('199.00'),
                'stock': 10,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1566882168631-1a75c89d6fd0?w=600'
            },
            {
                'category': plants,
                'name': 'Money Plant',
                'slug': 'money-plant',
                'description': 'A gorgeous potted Epipremnum aureum (Money Plant) with trailing heart-shaped leaves splashed with gold. Perfect for bringing good fortune and green energy.',
                'price': Decimal('89.00'),
                'stock': 25,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600'
            },
            {
                'category': plants,
                'name': 'Jade Plant',
                'slug': 'jade-plant',
                'description': 'A resilient potted succulent Jade plant with thick glossy leaves and tree-like woody stems. Symbolizes prosperity, luck, and friendship.',
                'price': Decimal('99.00'),
                'stock': 16,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1459156212016-c812468e2115?w=600'
            },
            
            # GIFTS & ADD-ONS
            {
                'category': gifts,
                'name': 'Rose Gift Box',
                'slug': 'rose-gift-box',
                'description': 'An ultra-premium, elegant black gift box packed with fresh roses arranged meticulously. Perfect for sophisticated surprises and celebrations.',
                'price': Decimal('280.00'),
                'stock': 10,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600'
            },
            {
                'category': gifts,
                'name': 'Flower Hamper',
                'slug': 'flower-hamper',
                'description': 'An exquisite curated gift basket featuring fresh flowers, a selection of artisanal treats, and a premium scented lavender candle.',
                'price': Decimal('320.00'),
                'stock': 7,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1487530811015-780780fc54c2?w=600'
            },
            {
                'category': gifts,
                'name': 'Helium Balloon',
                'slug': 'helium-balloon',
                'description': 'A beautiful, floating helium balloon in pastel tones. Perfect add-on to elevate your floral surprise.',
                'price': Decimal('45.00'),
                'stock': 999,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=600'
            },
            {
                'category': gifts,
                'name': 'Luxury Chocolates',
                'slug': 'luxury-chocolates',
                'description': 'A curated box of delicious, artisanal Belgian luxury chocolates. A sweet accompaniment to your flower arrangements.',
                'price': Decimal('115.00'),
                'stock': 999,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=600'
            }
        ]

        # 3. Create Products
        for item in products_data:
            prod, created = Product.objects.get_or_create(
                slug=item['slug'],
                defaults={
                    'category': item['category'],
                    'name': item['name'],
                    'description': item['description'],
                    'price': item['price'],
                    'stock': item['stock'],
                    'is_featured': item['is_featured'],
                    'image_url': item['image_url']
                }
            )
            if not created:
                # Update details if already present
                prod.category = item['category']
                prod.name = item['name']
                prod.description = item['description']
                prod.price = item['price']
                prod.stock = item['stock']
                prod.is_featured = item['is_featured']
                prod.image_url = item['image_url']
                prod.save()
            self.stdout.write(f"Seeded Product: {prod.name} ({'Created' if created else 'Updated'})")

        self.stdout.write(self.style.SUCCESS('Successfully seeded the 18 premium products and add-ons in AED!'))
