from django.contrib import admin
from .models import Product, ProductCategory, ProductImage


# Inline-класс ProductImageInline показывает связанные записи прямо внутри страницы родительской модели в админке.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductCategory)
# Админ-класс ProductCategoryAdmin настраивает, как модель отображается и редактируется в панели Django admin.
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_name', 'product_category_slug', 'product_category_parent', 'product_category_order')
    prepopulated_fields = {'product_category_slug': ('product_category_name',)}


@admin.register(Product)
# Админ-класс ProductAdmin настраивает, как модель отображается и редактируется в панели Django admin.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_new_price', 'product_in_stock', 'product_stock_quantity')
    list_filter = ('product_category', 'product_in_stock')
    search_fields = ('product_name', 'product_description')
    prepopulated_fields = {'product_slug': ('product_name',)}
    inlines = [ProductImageInline]
