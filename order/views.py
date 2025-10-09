from urllib import request
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from cart.models import Cart, CartItem
from order.froms import CreateOrderForm
from order.models import Order, OrderItem

class CreateOrderView(LoginRequiredMixin, FormView):
  template_name = 'order/create_order.html'
  form_class = CreateOrderForm
  success_url = reverse_lazy('user:profile')

  def get_initial(self):
    initial = super().get_initial()
    initial['username'] = self.request.user.username
    return initial
  
  def form_valid(self, form):
    try:
      user = self.request.user
      cart = Cart.objects.get(user=user)
      cart_items = cart.items.all()

      if cart:
        # Создать заказ
        order = Order.objects.create(
          user=user,
          phone_number=form.cleaned_data["phone_number"],
          requires_delivery=form.cleaned_data["requires_delivery"],
          delivery_address=form.cleaned_data["delivery_address"],
        )

        for cart_item in cart_items:
          product = cart_item.product_variant.product
          name = f"{cart_item.product_variant.product.name} - {cart_item.product_variant.get_size_ml_display()}"
          price = cart_item.product_variant.sell_price()
          quantity = cart_item.quantity

          OrderItem.objects.create(
            order=order,
            product=product,
            name=name,
            price=price,
            quantity=quantity,
          )
          product.save()
        
        cart.delete()

        messages.success(self.request, "Заказ оформлен!")
        return redirect("user:profile")
    except ValidationError as e:
      messages.error(self.request, str(e))
      return redirect('order:create_order')
    
  def form_invalid(self, form):
    messages.error(self.request, 'Заполните все обязательные поля!')
    return redirect('order:create_order')
    
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Оформление заказа'
      return context

    
    

      
