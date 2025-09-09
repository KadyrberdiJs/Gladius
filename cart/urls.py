from django.urls import path

from gladius import settings
from django.conf.urls.static import static
from . import views

app_name = 'cart'

urlpatterns = [
  path('add/<slug:product_slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
  path('cart-detail/', views.CartDetailView.as_view(), name='cart-detail'),
]
