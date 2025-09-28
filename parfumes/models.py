from decimal import Decimal
from itertools import product
from tabnanny import verbose
from django.db import models
from django.urls import reverse


class Category(models.Model):
  name = models.CharField(max_length=100, unique=True, verbose_name='Название')
  slug = models.SlugField(max_length=150, unique=True, verbose_name='URL')

  is_active = models.BooleanField(default=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'category'
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
  
  def __str__(self):
      return self.name


class Product(models.Model):
   name = models.CharField(max_length=200, unique=True, verbose_name='Имя')
   slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
   brand_name = models.CharField(max_length=120, verbose_name='Имя бренда')
   price = models.DecimalField(default=0, max_digits=7, decimal_places=0, verbose_name='Цена')
   discount = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='Скидка в %')

   description = models.TextField(verbose_name='Описане')
   image = models.ImageField(upload_to='parfumes_images', verbose_name='Изображения')
   category = models.ForeignKey(to=Category,
                                on_delete=models.CASCADE, 
                                related_name='products',
                                verbose_name='Категория')
   is_active = models.BooleanField(default=True)
   is_featured = models.BooleanField(default=False)

   created_at = models.DateTimeField(auto_now_add=True)


   class Meta:
      db_table = 'product'    
      verbose_name = 'Продукт'
      verbose_name_plural = 'Продукты'
      ordering = ('-created_at',)
    
   def __str__(self):
     return self.name

   def sell_price(self):
    if self.discount and self.discount > 0: # если есть скидка
      return round(self.price - self.price * self.discount/100, 0) 
    return self.price


SIZE_MULTIPLIERS = {
  10: Decimal('1.0'),
  20: Decimal('1.944'),
  30: Decimal('2.778'),
  50: Decimal('4.444'),
}

class ProductVariant(models.Model):
   SIZE_CHOICES = [
     (10, '10ml'),
     (20, '20ml'),
     (30, '30ml'),
     (50, '50ml'),
   ]

   product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants',
                               verbose_name='Имя')
   size_ml = models.IntegerField(choices=SIZE_CHOICES, verbose_name='Объем (ml)')
   price = models.DecimalField(default=0, max_digits=7, decimal_places=0, 
                               verbose_name='Цена для этого размера')
   stock_quantity = models.PositiveIntegerField(default=0, 
                                                verbose_name='Количество на складе для этого размера')
   
   
   class Meta:
     unique_together = ['product', 'size_ml']
     verbose_name = 'Вариант продукта'
     verbose_name_plural = 'Вариант продуктов'
   
   def __str__(self):
      return f"{self.product.name} - {self.get_size_ml_display()}"
   
   def sell_price(self):
    if self.product.discount: # если есть скидка
      return round(self.price - self.price * self.product.discount/100, 0) 
    return self.price
   
   def save(self, *args, **kwargs):
      if not self.price or self.pk is None:
        base_price = self.product.price
        multiplier = SIZE_MULTIPLIERS.get(self.size_ml, Decimal('1.0'))
        self.price = round(base_price * multiplier)
      super().save(*args, **kwargs) 


   def is_in_stock(self, quantity):
     return self.stock_quantity >= quantity
  
   


  #  def __str__(self):
  #   return f"{self.name} - {self.brand_name}"
   
  #  def get_absolute_url(self):
  #    return reverse("catalog:products", kwargs={"product_slug": self.slug})