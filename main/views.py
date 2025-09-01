from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from parfumes.models import Product


class HomeView(TemplateView):
  template_name = 'base.html'


  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      featured_products = Product.objects.filter(is_featured=True)
      discount_products = Product.objects.filter(discount__gt=0)
      elite_products = Product.objects.filter(slug='isola-blu')
      hero_product = Product.objects.filter(slug='tygar')
      
      context['title'] = 'Gladius'
      context['hero_parfume'] = hero_product
      context['featured_parfumes'] = featured_products
      context['discount_parfumes'] = discount_products
      context['elite_parfumes'] = elite_products

      return context

  
  
