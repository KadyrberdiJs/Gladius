from email.policy import default
from gc import get_objects
from os import name
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.db.models import Q  

from parfumes.models import Product, Category, ProductVariant


class CatalogView(ListView):

  model = Product
  template_name = 'parfumes/catalog.html'
  context_object_name = 'parfumes'
  paginate_by = 12

  def get_queryset(self):
      queryset = super().get_queryset()

      category_slug = self.kwargs.get('category_slug')
      
      if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug).order_by('brand_name')
        
      sort_by = self.request.GET.get('sort_by')

      if sort_by == 'relevant':
          queryset = queryset.order_by('brand_name')

      if sort_by == 'HighestPrice':
          queryset = queryset.order_by('-price')

      if sort_by == 'LowestPrice':
          queryset = queryset.order_by('price')

      if sort_by == 'on_sale':
          queryset = queryset.filter(discount__gt=0).order_by('-discount')
      
      search_query = self.request.GET.get('search')

      if search_query:
          queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(brand_name__icontains=search_query))
        
      return queryset



  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      category_slug = self.kwargs.get('category_slug')
      context['slug_url'] = category_slug
      
      if category_slug == 'all':
          context['title'] = 'Все парфюмы'
          context['page_title'] = 'Полный каталог ароматов'
      elif category_slug == 'universalnyj':
          context['title'] = 'Универсальные парфюмы'
          context['page_title'] = 'Универсальные ароматы'
      
      elif category_slug == 'muzhskoj':
          context['title'] = 'Мужские парфюмы'
          context['page_title'] = 'Мужские ароматы'
      
      elif category_slug == 'zhenskij':
          context['title'] = 'Женские парфюмы'
          context['page_title'] = 'Женские ароматы'
          

      return context
  

def product_detail(request, product_slug):
    parfume = get_object_or_404(Product, slug=product_slug)
    default_variant = parfume.variants.filter(size_ml=10).first()
    context = {
        'parfume': parfume,
        'default_variant': default_variant,
        'variants': parfume.variants.all(),
        'title': f'Gladius - {parfume.brand_name} {parfume.name}'
    }

    return render(request, 'parfumes/product.html', context)



def get_variant_price(request, product_id, size_ml):
    product = get_object_or_404(Product, id=product_id)
    try:
        variant = product.variants.get(size_ml=size_ml)
        price = variant.price
        sell_price = variant.sell_price()
        has_discount = bool(product.discount)
        return JsonResponse({
            'price': float(sell_price),
            'original_price': price if has_discount else None,
            'has_discount': has_discount
        })
    except ProductVariant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=400)







# class ProductView(DetailView):

#     template_name = 'parfumes/product.html'
#     slug_url_kwarg = 'product_slug'
#     context_object_name = 'parfume'
    
#     def get_object(self, queryset = None):
#         parfume = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
#         return parfume
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = self.object.name
#         return context
    