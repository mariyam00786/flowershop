from django.core.management.base import BaseCommand
from store.models import Category, Product
from orders.models import Coupon
from django.utils import timezone
from decimal import Decimal
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with beautiful initial flower categories, products, and test coupons.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding categories...')
        
        # 1. Categories
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

        self.stdout.write('Seeding products...')

        # 2. Bouquets
        Product.objects.get_or_create(
            category=bouquets,
            name='Enchanted Rose Cascade',
            slug='enchanted-rose-cascade',
            description='A luxurious arrangement of 24 fresh crimson red roses, hand-styled with baby breath and silver dollar eucalyptus in our signature soft pink wrapping. Perfect for romantic gestures.',
            price=Decimal('1299.00'),
            stock=15,
            is_featured=True
        )
        Product.objects.get_or_create(
            category=bouquets,
            name='Pastel Harmony Bouquet',
            slug='pastel-harmony-bouquet',
            description='A soothing blend of soft pink carnations, peach roses, white lilies, and lavender sprigs. Hand-tied with sage green velvet ribbons for a elegant present.',
            price=Decimal('949.00'),
            stock=8,
            is_featured=True
        )
        Product.objects.get_or_create(
            category=bouquets,
            name='Sunlit Meadow Delight',
            slug='sunlit-meadow-delight',
            description='Brighten up any room with our vibrant selection of sunflowers, yellow gerberas, and daisy chrysanthemums coupled with wild greens.',
            price=Decimal('799.00'),
            stock=20,
            is_featured=False
        )

        # 3. Single Flowers
        Product.objects.get_or_create(
            category=single_flowers,
            name='Premium Crimson Stem Rose',
            slug='premium-crimson-stem-rose',
            description='A single, long-stemmed Ecuadorian red rose of pristine grade, packaged individually in an elegant clear presentation sleeve with a silk bow.',
            price=Decimal('149.00'),
            stock=50,
            is_featured=False
        )
        Product.objects.get_or_create(
            category=single_flowers,
            name='Royal Purple Orchid stem',
            slug='royal-purple-orchid-stem',
            description='A stunning exotic single stem of deep violet Phalaenopsis orchids with multiple blooms. Durable and absolutely gorgeous.',
            price=Decimal('299.00'),
            stock=30,
            is_featured=True
        )

        # 4. Plants
        Product.objects.get_or_create(
            category=plants,
            name='Sleek Monstera Deliciosa',
            slug='sleek-monstera-deliciosa',
            description='Bring the tropics indoors with a healthy, potted Monstera plant. Famous for its iconic leaf splits and easy-care nature. Comes in a sage green ceramic planter.',
            price=Decimal('849.00'),
            stock=12,
            is_featured=True
        )
        Product.objects.get_or_create(
            category=plants,
            name='Pristine Peace Lily Pot',
            slug='pristine-peace-lily-pot',
            description='A beautiful air-purifying Peace Lily plant with lush green leaves and majestic white spathes. Perfectly potted in a white clay pot.',
            price=Decimal('549.00'),
            stock=18,
            is_featured=False
        )

        # 5. Gifts
        Product.objects.get_or_create(
            category=gifts,
            name='Gourmet Chocolate & Blossom Hamper',
            slug='gourmet-chocolate-blossom-hamper',
            description='A premium wicker basket featuring a petite arrangement of pastel roses, a box of luxury Belgian truffles, and a scented lavender candle.',
            price=Decimal('1899.00'),
            stock=10,
            is_featured=True
        )
        Product.objects.get_or_create(
            category=gifts,
            name='Lavender Fields Scented Candle',
            slug='lavender-fields-scented-candle',
            description='A clean-burning soy wax candle infused with organic french lavender essential oils, hand-poured in a custom glass jar. Burns for up to 40 hours.',
            price=Decimal('349.00'),
            stock=40,
            is_featured=False
        )

        self.stdout.write('Seeding Coupons...')

        # 6. Coupons
        Coupon.objects.get_or_create(
            code='FLOWERS10',
            discount_percent=10,
            max_uses=100,
            valid_until=timezone.now() + datetime.timedelta(days=90),
            is_active=True
        )
        Coupon.objects.get_or_create(
            code='ROSEIVY20',
            discount_percent=20,
            max_uses=500,
            valid_until=timezone.now() + datetime.timedelta(days=90),
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded Rose & Ivy database!'))
