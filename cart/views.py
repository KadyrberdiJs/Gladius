from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart, CartItem
from parfumes.models import Product, ProductVariant


def add_to_cart(request, product_id):
  """
  This view handles when someone clicks "Add to cart"
  It captures both size choices and quantity
  """

  if request.method == 'POST':
    # Get the main product
    product = get_object_or_404(Product, id=product_id)

    # Get the specific size they selected form the form
    size_ml = request.POST.get('size_ml')
    quantity = int(request.POST.get('quantity', 1))

    # Find the exact variant they want 
    try:
      product_variant = ProductVariant.objects.get(
        product=product,
        size_ml=size_ml
      )
    except ProductVariant.DoesNotExist:
      messages.error(request, f'Sorry, {product.name} in {size_ml}ml is not available')
      return redirect('product_detail', product_id=product.id)
    
    # Chect if we have enough stcok
    if not product_variant.is_in_stock(quantity):
      messages.error(request, f"Sorry, we only have {product_variant.stock_quantity} units of {product_variant} in stock.")
      return redirect('product_detail', product_id=product.id)
    
    # Get or create cart for this user
    cart = get_or_create_cart(request)

    # Try to get existing cart item (maybe they added this variant before)
    cart_item, created = CartItem.objects.get_or_create(
      cart=cart, 
      product_variant=product_variant,
      defaults={'quantity': quantity} # if creating new, use this quantity
    )

    if not created:
      # They already  had this variant in cart, so add to existing quantity
      cart_item.quantity += quantity

      # Make sure we dont exceed available stcok
      if not product_variant.is_in_stock(cart_item.quantity):
        messages.error(request, f"Sorry, we only have {product_variant.stock_quantity} units available.")
        return redirect('cart_detail')
      
      cart_item.save()
      messages.success(request, f'Updated {product_variant} quantity to {cart_item.quantity}')
    else:
      # This is a new item in their cart
      messages.success(request, f"Added {quantity} * {product_variant} to your cart")

    return redirect('cart_detail')
  return redirect('product_detail')
      
def get_or_create_cart(request):
  """
  Helper function to get users cart 
  Creates new cart if they dont have one
  """
  if request.user.is_authenticated:
    # For logged-in users, use their user account 
    cart, created = Cart.objects.get_or_create(user=request.user)
  else:
    # For anonymus users, use session 
    session_key = request.session.session_key
    if not session_key:
      request.session.create()
      session_key = request.session.session_key
      
      cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart
  
def cart_detail(request):
  """
  Show all items in users cart with full details
  This is where you can see the size and quantity clearly
  """

  cart = get_or_create_cart(request)
  cart_items = cart.items.all()

  # Build detailed info for each item
  items_data = []
  for item in cart_items:
    items_data.append({
      'product_name': item.product_variant.product.name,
      'brand': item.product_variant.product.brand_name,
      'size_ml': item.product_variant.size_ml,
      'size_display': item.product_variant.get_size_ml_display(),
      'quantity': item.quantity,
      'unit_price': item.product_variant.price,
      'total_price': item.get_total_price(),
      'item_id': item.id,
    })

  context = {
    'cart': cart,
    'cart_items': cart_items,
    'items_data': items_data,
    'total_price': cart.get_total_price(),
    'total_items': cart.get_total_items()
  }

  return render(request, 'cart/cart_detail.html', context)