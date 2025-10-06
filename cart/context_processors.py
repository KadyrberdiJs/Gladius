from cart.models import Cart


def cart_context(request):
  cart = None
  if request.user.is_authenticated:
    cart = Cart.objects.filter(user=request.user).first()
  else:
    session_key = request.session.session_key
    if not session_key:
      request.session.create()
      session_key = request.session.session_key
      
    cart = Cart.objects.filter(session_key=session_key).first()
  
  total_items = 0
  if cart:
    total_items = sum(item.quantity for item in cart.items.all())

  return {'total_items': total_items}