from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from cart.mixins import CartMixin
from cart.models import Cart, CartItem
from parfumes.models import Product, ProductVariant

from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from cart.mixins import CartMixin
from cart.models import Cart, CartItem
from parfumes.models import Product, ProductVariant

class AddToCartView(CartMixin, View):
    def post(self, request, product_id):
        # Get the product
        product = get_object_or_404(Product, id=product_id)

        # Get size and quantity from the form
        size_ml = request.POST.get('size_ml')
        quantity = int(request.POST.get('quantity', 1))


        # Find the product variant
        try:
            product_variant = ProductVariant.objects.get(
                product=product,
                size_ml=size_ml
            )
        except ProductVariant.DoesNotExist:
            return self.handle_response(
                request, product, success=False,
                message=f'Извините, {product.name} в {size_ml} ml не доступен.'
            )


        # Check stock (allow adding up to the available stock)
        if product_variant.stock_quantity < quantity:
            return self.handle_response(
                request, product, success=False,
                message=f'Извините, доступно только {product_variant.stock_quantity} единиц.'
            )

        # Get or create cart
        cart = self.get_or_create_cart(request)

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )

        if not created:
            # Item already existed, so update the quantity
            new_quantity = cart_item.quantity + quantity
        
            if product_variant.stock_quantity < quantity:
                return self.handle_response(
                    request, product, success=False,
                    message=f'Извините, на складе осталось только {product_variant.stock_quantity} единиц {product.name}.'
                )

            cart_item.quantity = new_quantity
            cart_item.save()
            product_variant.stock_quantity -= quantity
            product_variant.save()
            return self.handle_response(
                request, product, success=True,
                message=f"Товар обновлён."
            )
        else:
            product_variant.stock_quantity -= quantity
            product_variant.save()
            return self.handle_response(
                request, product, success=True,
                message=f"Товар добавлен"
            )

    def handle_response(self, request, product, success, message):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': message
            })
        else:
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            context = {
                'parfume': product,
                'title': product.name,
            }
            return render(request, 'parfumes/product.html', context)




class CartDetailView(CartMixin, TemplateView):
  template_name = 'cart/cart_detail.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Gladius - Корзина'
      
      cart = self.get_or_create_cart(self.request)
      cart_items = cart.items.all()
      items_data = []
      for item in cart_items:
        items_data.append({
          'product_name': item.product_variant.product.name,
          'brand': item.product_variant.product.brand_name,
          'image': item.product_variant.product.image,
          'size_ml': item.product_variant.size_ml,
          'size_display': item.product_variant.get_size_ml_display(),
          'quantity': item.quantity,
          'unit_price': item.product_variant.price,
          'total_price': item.get_total_price(),
          'item_id': item.id,
        })
      context.update({
        'cart': cart,
        'cart_items': cart_items,
        'items_data': items_data,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
      })

      return context
  