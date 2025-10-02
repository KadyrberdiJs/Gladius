from django.contrib import messages
from django.shortcuts import render
from cart.models import Cart
from django.http import JsonResponse

class CartMixin:
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
    
    def handle_response(self, request, product, success, message):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': message,
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


