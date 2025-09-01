from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from cart.models import Cart, CartItem
from parfumes.models import Product, ProductVariant

class AddToCartView(View):
  def post(self, request, product_id):
    # Get the product
    product = get_object_or_404(Product, id=product_id)

    # Get size and quantity from the form
    size_ml = request.POST.get('size_ml')
    
    try:
      quantity = int(request.POST.get('quantity', 1))
      if quantity <= 0:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect('product', product_id=product.id)
    except ValueError:
      messages.error(request, 'Invalid quantity entered.')
      return redirect('product', product_id=product.id)
    
    

    #Find the product variant 
    try: 
      product_variant = ProductVariant.objects.get(
        product=product,
        size_ml=size_ml
      )
    except ProductVariant.DoesNotExist:
      messages.error(request, f'Sorry {product.name} in {size_ml}ml is not available')
      return redirect('parfumes:product', product_id=product.id)
    
    # Check stock (using Product's stock_quantity for now)
    if product.stock_quantity < quantity:
      messages.error(request, f'Sorry, only {product.stock_quantity} available')
      return redirect('product', product_id=product.id)
    
    # Get or create cart
    cart = self.get_or_create_cart(request)

    # Addd or update  cart item
    cart_item, created = CartItem.objects.get_or_create(
      cart=cart,
      product_variant=product_variant,
      defaults={'quantity':quantity}
    )

    if not created:
      # Item already existed, so update the quantity
      new_quantity = cart_item.quantity + quantity
      if product.stock_quantity < new_quantity:
        messages.error(request, f'Sorry, only {product.stock_quantity} units of {product.name} are in stock')
        return redirect('cart_detail')
      
      cart_item.quantity = new_quantity
      cart_item.save()
      messages.success(request, f"Updated {product_variant} to {cart_item.quantity} in your cart")
    else:
      messages.success(request, f"Added {quantity} x {product_variant} to your cart.")
    
    return redirect('cart_detail')
  
  def get_or_create_cart(self, request):
    if request.user.is_authenticated:
      cart, created = Cart.objects.get_or_create(user=request.user)
    else:
      session_key = request.session.session_key
      if not session_key:
        request.session.create()
        session_key = request.session.session_key
      cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


  
