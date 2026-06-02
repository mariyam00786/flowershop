from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with exactly the requested premium flower and add-on products with real Unsplash photo URLs and AED pricing.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Preparing to seed premium flower-only products in AED...')

        # 1. Ensure active Categories exist by slug (unique field)
        bouquets, _ = Category.objects.get_or_create(
            slug='bouquets',
            defaults={'name': 'Bouquets'}
        )
        single_flowers, _ = Category.objects.get_or_create(
            slug='single-flowers',
            defaults={'name': 'Single Flowers'}
        )
        gifts, _ = Category.objects.get_or_create(
            slug='gifts',
            defaults={'name': 'Gifts'}
        )

        # Force naming matching user requirements
        bouquets.name = 'Bouquets'
        bouquets.save()
        single_flowers.name = 'Single Flowers'
        single_flowers.save()
        gifts.name = 'Gifts'
        gifts.save()

        self.stdout.write('Clearing categories other than Bouquets, Single Flowers, and Gifts...')
        Category.objects.exclude(slug__in=['bouquets', 'single-flowers', 'gifts']).delete()

        self.stdout.write('Clearing old products to ensure clean seed state...')
        Product.objects.all().delete()

        # 2. Product definitions matching requested inventory exactly
        products_data = [
            # === BOUQUETS ===
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
                'name': 'Pink Peony Bouquet',
                'slug': 'pink-peony-bouquet',
                'description': 'A luxurious and soft arrangement of pillowy, fresh pink peonies, beautifully styled in our signature wrapping paper. Perfect for high-end gifting.',
                'price': Decimal('399.00'),
                'stock': 8,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1589994160839-163cd867cfe8?w=600'
            },
            {
                'category': bouquets,
                'name': 'Tulip Bouquet',
                'slug': 'tulip-bouquet',
                'description': 'A beautifully crisp, fresh arrangement of premium tulips. Colorful, elegant, and classic addition to any premium home.',
                'price': Decimal('220.00'),
                'stock': 18,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1561328399-f94d2ce78679?w=600'
            },
            {
                'category': bouquets,
                'name': 'White Rose Bouquet',
                'slug': 'white-rose-bouquet',
                'description': 'An opulent arrangement of pure white premium roses, hand-styled for high-end gifting. Elegance at its finest.',
                'price': Decimal('350.00'),
                'stock': 12,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=600'
            },
            
            # === SINGLE FLOWERS ===
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
                'name': 'Purple Lavender',
                'slug': 'purple-lavender',
                'description': 'A fragrant bundle of dried premium French purple lavender stems, popular for its soothing aromatherapy benefits and rustic visual charm.',
                'price': Decimal('79.00'),
                'stock': 28,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1611909023032-2d6b3134ecba?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Blue Iris Single',
                'slug': 'blue-iris-single',
                'description': 'An exotic single stem of deep blue iris featuring striking purple-blue petals highlighted with bright golden-yellow markings.',
                'price': Decimal('65.00'),
                'stock': 15,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Red Gerbera Single',
                'slug': 'red-gerbera-single',
                'description': 'A cheerful and large-flowered single stem of bright red Gerbera daisy, guaranteed to uplift spirits with its bold color.',
                'price': Decimal('55.00'),
                'stock': 20,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?w=600'
            },
            {
                'category': single_flowers,
                'name': 'Pink Carnation Single',
                'slug': 'pink-carnation-single',
                'description': 'A delicate, long-stemmed single pink carnation, expressing deep admiration, love, and gratitude.',
                'price': Decimal('49.00'),
                'stock': 30,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1487530811015-780780fc54c2?w=600'
            },
            
            # === GIFTS ===
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
                'name': 'Luxury Flower Box',
                'slug': 'luxury-flower-box',
                'description': 'An exquisite presentation of fresh premium flowers arranged meticulously in our signature luxury gift box.',
                'price': Decimal('450.00'),
                'stock': 10,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600'
            },
            {
                'category': gifts,
                'name': 'Anniversary Flower Hamper',
                'slug': 'anniversary-flower-hamper',
                'description': 'The ultimate romance gift basket loaded with fresh roses, floral treats, and premium accents. Perfect for marking milestones.',
                'price': Decimal('599.00'),
                'stock': 5,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1487530811015-780780fc54c2?w=600'
            },
            {
                'category': gifts,
                'name': 'Birthday Bouquet Box',
                'slug': 'birthday-bouquet-box',
                'description': 'A gorgeous birthday curation featuring a fresh premium bouquet and upscale treats presented beautifully in our custom card box.',
                'price': Decimal('380.00'),
                'stock': 8,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=600'
            },
            
            # === UPSELL ADD-ONS (Seeded under Gifts) ===
            {
                'category': gifts,
                'name': 'Rose Water Spray',
                'slug': 'rose-water-spray',
                'description': 'Premium organic rose water spray flower care add-on. Essential for keeping fresh cuts hydrated.',
                'price': Decimal('35.00'),
                'stock': 999,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=600'
            },
            {
                'category': gifts,
                'name': 'Gift Ribbon & Card',
                'slug': 'gift-ribbon-card',
                'description': 'High-quality luxury satin gift ribbon and greeting card wrapping add-on. Customizable on demand.',
                'price': Decimal('25.00'),
                'stock': 999,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=600'
            },
            {
                'category': gifts,
                'name': 'Flower Food Sachet',
                'slug': 'flower-food-sachet',
                'description': 'Freshness flower food sachet add-on to extend bloom life in your signature vase.',
                'price': Decimal('15.00'),
                'stock': 999,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1561328399-f94d2ce78679?w=600'
            }
        ]

        # 3. Create Products in the database
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
                # Update details if already present to reflect clean seed state
                prod.category = item['category']
                prod.name = item['name']
                prod.description = item['description']
                prod.price = item['price']
                prod.stock = item['stock']
                prod.is_featured = item['is_featured']
                prod.image_url = item['image_url']
                prod.save()
            self.stdout.write(f"Seeded Product: {prod.name} ({'Created' if created else 'Updated'})")

        self.stdout.write(self.style.SUCCESS('Successfully seeded premium flower-only boutique in AED!'))
