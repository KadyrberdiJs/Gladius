from django.contrib import admin

from cart.models import Cart, CartItem
from cart.views import AddToCartView, CartDetailView


@admin.register(Cart)
class AddToCartAdmin(admin.ModelAdmin):
  list_display = ['user']


@admin.register(CartItem)
class AddToCartAdmin(admin.ModelAdmin):
  list_display = ['cart', 'product_variant']