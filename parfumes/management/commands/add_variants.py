from decimal import Decimal

from django.core.management.base import BaseCommand
from parfumes.models import SIZE_MULTIPLIERS, Product, ProductVariant


SIZE_MULTIPLIERS = {
  10: Decimal('1.0'),
  20: Decimal('1.944'),
  30: Decimal('2.778'),
  50: Decimal('4.444'),
}

class Command(BaseCommand):
  help = 'Add ProductVariant objects for existing products'

  def handle(self, *args, **kwargs):
    products = Product.objects.all()
    count = 0
    for product in products:
      if not product.variants.exists():
        for size in [10, 20, 30, 50]:
          ProductVariant.objects.create(
            product=product,
            size_ml=size,
            price=round(product.price * SIZE_MULTIPLIERS[size]),
            stock_quantity=10,
          )
          count += 1
        self.stdout.write(self.style.SUCCESS(f'Added variants for {product.name}'))
      else:
        self.stdout.write(f'Skipped {product.name} (already has variants)')
    self.stdout.write(self.style.SUCCESS(f'Created {count} variants for {len(products)} products'))

      