from django.contrib import admin

from parfumes.models import Category, Product


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

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
          "fields": ('name', 'slug', 'description','category', 'image', 'price', 'discount'),
      }),
      ('Details', {
        "fields": ('stock_quantity', 'is_active', 'is_featured')
      })
  )
  
