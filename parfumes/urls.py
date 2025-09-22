from django.urls import path

from gladius import settings
from django.conf.urls.static import static
from . import views

app_name = 'catalog'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/all/', views.CatalogView.as_view(), name='catalog_all'),
    path('product/<int:product_id>', views.product_detail, name='product_detail'),
    path('get-price/<int:product_id>/<int:size_ml>/', views.get_variant_price, name='get_variant_price'),
]
