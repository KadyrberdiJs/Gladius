from django.db.models.signals import post_save
from django.dispatch import receiver

from parfumes.models import SIZE_MULTIPLIERS, Product, ProductVariant


@receiver(post_save, sender=Product)
def create_variants(sender, instance, created, **kwargs):
  if created:
    sizes = [10, 20, 30, 50] # Matches SIZE_CHOICES
    for size in sizes:
      ProductVariant.objects.create(
        product = instance,
        size_ml = size,
        price = round(instance.price * SIZE_MULTIPLIERS[size]),
        stock_quantity = 50,
      ) # Price will auto-calculate in save()