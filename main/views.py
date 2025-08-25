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
      
      context['hero_parfume'] = [
         {
            'name': 'Bvlgari Tygar',
            'description': 'В созданной известным парфюмером Жаком Кавалье ароматической композиции красиво переплетаются освежающие цитрусовые ноты розового грейпфрута и бархатисто-пряного запаха древесины',
            'image': 'static/images/parfumes/tygar-bvlgari.png'
         }
      ]
      # For now, we'll use static data that matches your template
        # Later, these will come from your database
      context['title'] = 'Gladius'
      context['featured_parfumes'] = featured_products
      context['discount_parfumes'] = discount_products
      context['elite_parfumes'] = elite_products

      return context

  
  
