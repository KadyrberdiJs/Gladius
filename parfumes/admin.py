from django.contrib import admin

from parfumes.models import Category, Product, ProductVariant


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

class ProductVariantInline(admin.TabularInline):
  model = ProductVariant
  extra = 1
  fields = ('size_ml', 'price', 'stock_quantity')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name",)}
  list_display = ('name','brand_name', 'price','category', 'is_active',)
  # list_editable = ('price', 'is_active')  
  list_filter = ('brand_name', 'is_active', 'is_featured',)
  search_fields = ('name', 'brand_name',)

  # fields = ('name', 'slug', 'brand_name', 'description', 'image', 'price', 'discount', 'stock_quantity', 'category', ('is_active', 'is_featured'),)
  fieldsets = (
      ('Parfume information', {
          "fields": ('name', 'slug', 'brand_name', 'description','category', 'image', 'price', 'discount'),
      }),
      ('Details', {
        "fields": ( 'is_active', 'is_featured')
      })
  )
  inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
  list_display = ['product', 'size_ml',  'price']
  list_editable = ['price']
  list_filter = ['product', 'size_ml']
  search_fields = ['product', 'size_ml']
  