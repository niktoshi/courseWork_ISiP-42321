from django.contrib import admin
from .models import Cart, CartItem


# Inline-класс CartItemInline показывает связанные записи прямо внутри страницы родительской модели в админке.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
# Админ-класс CartAdmin настраивает, как модель отображается и редактируется в панели Django admin.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'created_at', 'updated_at')
    inlines = [CartItemInline]
