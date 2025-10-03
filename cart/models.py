from django.db import models

from parfumes.models import ProductVariant
from user.models import User


class Cart(models.Model):
  user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
  session_key = models.CharField(max_length=40, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
  updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменение')

  def __str__(self):
    if self.user:
      return f"Cart for {self.user.username}"
    return f'Анонимная корзина {self.id}'
  
  def get_total_items(self):
    return sum(item.quantity for item in self.items.all())

  def get_total_price(self):
    return sum(item.get_price() for item in self.items.all())  
  

class CartItem(models.Model):
  cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='items')
  product_variant = models.ForeignKey(to=ProductVariant, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
  added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')

  class Meta:
    unique_together = ['cart', 'product_variant']

  def __str__(self):
    return f"{self.quantity} x {self.product_variant}"
  
  def get_price(self):
    return self.product_variant.price * self.quantity
  
