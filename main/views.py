from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from parfumes.models import Product


class HomeView(TemplateView):
  template_name = 'base.html'


  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
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
      context['featured_parfumes'] = [
            {
                'name': 'Bleu De Chanel',
                'brand': 'Chanel', 
                'price': 100.00,
                'image': 'static/images/parfumes/Chanel Bleu De Chanel.png'
            },
            {
                'name': 'Creed Aventus',
                'brand': 'Creed',
                'price': 350.00, 
                'image': 'static/images/parfumes/creed-aventus.png'
            },
            {
                'name': "l'immensite",
                'brand': 'Louis vuitton',
                'price': 250.00,
                'image': 'static/images/parfumes/limminsite.png'
            },
            {
                'name': 'Imagination',
                'brand': 'Louis vuitton', 
                'price': 120.00,
                'image': 'static/images/parfumes/imagination.png'
            }
        ]

      return context

  
  
